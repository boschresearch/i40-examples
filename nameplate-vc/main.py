# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/IDunion/i40-examples
#
# SPDX-License-Identifier: Apache-2.0

import os
import json
from datetime import datetime
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

import ssi
import templates
import aas
import db
import b64
import endpoints
import demo
from models import Nameplate, Tenant
from dependencies import DB_KEY_PREFIX_VC, DB_KEY_PREFIX_VP, settings

app = FastAPI(title="Nameplate-VC - DPP Digital Product Passport Demo with Verifiable Credentials")


# TODO: for development, fix in production
origins = [
    "*",
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"])

app.include_router(demo.router)

app.include_router(ssi.router)
app.include_router(endpoints.router)


from pydantic import BaseModel, Field

class SelfSignFromRegistry(BaseModel):
    aas_id: str
    registry_base_url: str = settings.registry_base_url
    create_as_verifiable_presentation: bool = True
    store: bool = Field(default=True, description='store: Default is True. It will return the URL where it is stored. If False, the document itself will be returned')


@app.post('/{tenant_id}/issuevc/{connection_id}')
def issue_vc(tenant_id: str, connection_id: str, key_value:list = Body(...)):
    """
    Create and issue a VC from the input data (body) and send it to the given
    connection.

    In the future, the content of the requested VC AND the connection to which the VC
    is issued need to be checked.

    body: The content from a Submodel Namplate response, requested with "content=value"
    """
    data = ssi.prepare_vc(tenant_id=tenant_id, key_value_nameplate=key_value, connection_id=connection_id)
    print("Nameplate VC Data:")
    print(json.dumps(data, indent=4))
    result = ssi.issue_vc(tenant_id=tenant_id, vc=data)
    return result

def store_doc(item, aas_id: str):
    """
    Store the VC or VP for later fetch from the AAS submodel endpoints.
    Create a uuid under which it can be accessed.
    """
    id = str(uuid4())
    db.set_item(key=id, item=item, dbname=settings.db_name_credentials)
    # we also store a mapping from the aas_id - plain
    db.set_item(key=aas_id, item=item, dbname=settings.db_name_credentials)

    return id

def prepare_endpoint_url(id: str, is_vp: bool):
    if is_vp:
        return f"{settings.endpoint_base_url}/selfdescription/{id}"
    
    return f"{settings.endpoint_base_url}/nameplatevc/{id}"


@app.post('/{tenant_id}/selfsignfromregistry', tags=['main'])
def self_sign_from_registry(
    tenant_id: str,
    body: SelfSignFromRegistry = Body(...)
    ):
    """
    aas_id: from which we find the nameplate submodel that we use to sign the VC/VP
    registry_base_url: find the aas_id on this registry (if different to the default set via ENV var). needs to be publicly accessible
    create_as_verifiable_presentation: Return as VC or VP
    """
    nameplate = aas.get_nameplate_from_registry(aas_id=body.aas_id, registry_base_url=body.registry_base_url)
    signed = ssi.self_sign_vc(
        tenant_id=tenant_id,
        subject_identifier=body.aas_id,
        create_as_verifiable_presentation=body.create_as_verifiable_presentation,
        key_value=nameplate
    )
    if body.store:
        id = store_doc(signed, body.aas_id)
        url = prepare_endpoint_url(id=id, is_vp=body.create_as_verifiable_presentation)
        return {'url': url}

    return signed

# create demo user if not exists yet
ssi.create_tenant(tenant_id='demo')

if __name__ == '__main__':
    import uvicorn
    port = os.getenv('PORT', '8080')
    workers = os.getenv('WORKERS', '1')
    uvicorn.run("main:app", host="0.0.0.0", port=int(port), workers=int(workers), reload=False)
