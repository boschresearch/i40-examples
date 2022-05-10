# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/IDunion/i40-examples
#
# SPDX-License-Identifier: Apache-2.0

from fastapi import APIRouter, Body
import endpoints
import ssi

router = APIRouter(tags=['demo'])

@router.get('/demo/selfdescriptiononthefly/{b64_registry_base_url}/{b64_urlenc_aas_id}')
def get_selfdescription_on_the_fly(b64_registry_base_url: str, b64_urlenc_aas_id: str):
    """
    Creates a Self-Description (Verifiable Presenation) from the given aas_id's Nameplate
    on the fly

    b64_registry_base_url: Example:
    https://registry.h2894164.stratoserver.net -> aHR0cHM6Ly9yZWdpc3RyeS5oMjg5NDE2NC5zdHJhdG9zZXJ2ZXIubmV0

    b64_urlenc_aas_id: Example:
    http://boschrexroth.com/shells/0608842005/917004878 -> aHR0cDovL2Jvc2NocmV4cm90aC5jb20vc2hlbGxzLzA2MDg4NDIwMDUvOTE3MDA0ODc4

    """

    return endpoints.get_selfdescription_on_the_fly(
        tenant_id='demo',
        b64_registry_base_url=b64_registry_base_url,
        b64_urlenc_aas_id=b64_urlenc_aas_id
    )

@router.post('/demo/selfdescription')
def create_selfdescription(aas_id:str, key_value:list = Body(...)):
    """
    body: The content from a Submodel Namplate response, requested with "content=value"

    Example:

    aas_id: http://boschrexroth.com/shells/0608842005/917004878 -> aHR0cDovL2Jvc2NocmV4cm90aC5jb20vc2hlbGxzLzA2MDg4NDIwMDUvOTE3MDA0ODc4

    Copy content from:

    https://swagger.h2894164.stratoserver.net/shells/aHR0cDovL2Jvc2NocmV4cm90aC5jb20vc2hlbGxzLzA2MDg4NDIwMDUvOTE3MDA0ODc4/aas/submodels/aHR0cDovL2Jvc2NocmV4cm90aC5jb20vc2hlbGxzLzA2MDg4NDIwMDUvOTE3MDA0ODc4L3N1Ym1vZGVscy9uYW1lcGxhdGU/submodel/submodel-elements?content=value

    """
    selfdescription = ssi.self_sign_vc(tenant_id='demo', subject_identifier=aas_id, create_as_verifiable_presentation=True, key_value=key_value)
    return selfdescription

@router.post('/demo/verify')
def verify(doc: dict = Body(...)):
    """
    "outer_proof_verified" is the Verifiable Presentation

    "inner_proof" is the Verifiable Credential(s). The list is in the same order as the input. "all_inner_proofs" is a single value to check if ALL are verified.

    {
    "outer_proof_verified": true,
    "inner_proofs_verified": [
        true
    ],
    "all_inner_proofs_verified": true
    }
    """
    return ssi.verify_vc_or_vp(tenant_id='demo', doc=doc)