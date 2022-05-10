# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/IDunion/i40-examples
#
# SPDX-License-Identifier: Apache-2.0

from fastapi import APIRouter
import db
import ssi
import aas
import b64
from dependencies import DB_KEY_PREFIX_VC, DB_KEY_PREFIX_VP, settings

router = APIRouter()

@router.get('/{tenant_id}/selfdescription/{aas_id}', tags=['SubmodelEndpoints'])
def get_selfdescription(tenant_id: str, aas_id: str):
    """
    If stored in DB, return the Self-Description for the given AAS ID.

    Selfdescriptions are Verifiable Presentations (at least in Gaia-X context)

    TODO: do we need the tenant_id here?
    """
    item = db.get_item(key=DB_KEY_PREFIX_VP + aas_id, dbname=settings.db_name_credentials)
    return item


@router.get('/{tenant}/nameplatevc/{aas_id}', tags=['SubmodelEndpoints'])
def get_nameplat_vc(tenant_id: str, aas_id: str):
    """
    Here we return the pure VC (not a VP).
    """
    item = db.get_item(key=DB_KEY_PREFIX_VC + aas_id, dbname=settings.db_name_credentials)
    return item

@router.get('/{tenant_id}/selfdescriptiononthefly/{b64_registry_base_url}/{b64_urlenc_aas_id}')
def get_selfdescription_on_the_fly(tenant_id: str, b64_registry_base_url: str, b64_urlenc_aas_id: str):
    """
    Creates a Self-Description (Verifiable Presenation) from the given aas_id's Nameplate
    on the fly

    b64_registry_base_url: Example:
    https://registry.h2894164.stratoserver.net -> aHR0cHM6Ly9yZWdpc3RyeS5oMjg5NDE2NC5zdHJhdG9zZXJ2ZXIubmV0

    b64_urlenc_aas_id: Example:
    http://boschrexroth.com/shells/0608842005/917004878 -> aHR0cDovL2Jvc2NocmV4cm90aC5jb20vc2hlbGxzLzA2MDg4NDIwMDUvOTE3MDA0ODc4

    """
    aas_id = b64.decode(b64_data=b64_urlenc_aas_id)
    registry_base_url = b64.decode(b64_data=b64_registry_base_url)

    nameplate = aas.get_nameplate_from_registry(aas_id=aas_id, registry_base_url=registry_base_url)
    signed = ssi.self_sign_vc(
        tenant_id=tenant_id,
        subject_identifier=aas_id,
        create_as_verifiable_presentation=True,
        key_value=nameplate
    )
    return signed
