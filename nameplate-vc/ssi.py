# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/IDunion/i40-examples
#
# SPDX-License-Identifier: Apache-2.0

from uuid import uuid4
import secrets
import asyncio
from datetime import datetime
import requests
import json
from fastapi import APIRouter, Body

import db
import aas
import templates
from dependencies import settings, get_webhook_base_url
from models import Tenant, DidExchangeRequest, Nameplate

router = APIRouter()

def prepare_vc(tenant_id: str, key_value_nameplate:list, connection_id: str = ''):
    nameplate_dict = aas.convert_from_submodel_by_value_to_plain(key_value_nameplate)
    nameplate = Nameplate(**nameplate_dict)
    data = json.loads(templates.ISSUE_VC_TEMPLATE)
    nameplate_context = json.loads(templates.NAMEPLATE_CONTEXT)

    data['filter']['ld_proof']['credential']['@context'].append(nameplate_context)
    data['filter']['ld_proof']['credential']['type'].append(templates.NAMEPLATE_CREDENTIAL_TYPE)
    data['filter']['ld_proof']['credential']['credentialSubject'] = nameplate.dict()

    timestamp = datetime.now().isoformat(timespec='seconds')
    data['filter']['ld_proof']['credential']['issuanceDate'] = timestamp
    data['connection_id'] = connection_id
    tenant: Tenant = db.get_item(key=tenant_id, dbname=settings.db_name_tenants)
    did = prefix_did(tenant.did)
    data['filter']['ld_proof']['credential']['issuer'] = did

    return data

def self_sign_vc(
        tenant_id: str,
        subject_identifier: str,
        create_as_verifiable_presentation: bool = False,
        key_value:list = []
    ):
    """
    Used in the case the VC is NOT issued/sent to another identity.
    It is for signing VC for itself.

    subject_identifier: e.g. aas_id

    body: The content from a Submodel Namplate response, requested with "content=value"
    """
    result = None
    data = prepare_vc(tenant_id=tenant_id, key_value_nameplate=key_value)
    doc = data['filter']['ld_proof']['credential']
    doc['credentialSubject']['id'] = subject_identifier
    vc = self_sign(tenant_id=tenant_id, credential=doc)
    result = vc
    
    vp = None
    if create_as_verifiable_presentation:
        vp = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1"
            ],
            "type": "VerifiablePresentation",
            'verifiableCredential': [vc]
        }
        result = self_sign(tenant_id=tenant_id, credential=vp)

    return result


@router.post('/tenant')
async def create_new_tenant():
    """
    Creates a random new tenant id an checks the db if it exists
    returns the tenant_id
    """
    while(True):
        tenant_id = secrets.token_hex(3)
        if await create_tenant(tenant_id=tenant_id):
            return {'tenant': tenant_id }

async def create_tenant(tenant_id: str):
    """
    Create a Tenant
    Return: True if can be createcd
    False: if already exists and thus, can not be used
    """
    exists = db.key_in_db(key=tenant_id, dbname=settings.db_name_tenants)
    if exists:
        print(f"tenant with tenant_id: {tenant_id} already exists. Not creating it again.")
        return False

    db.set_item(key=tenant_id, item=Tenant(), dbname=settings.db_name_tenants)
    loop = asyncio.get_event_loop()
    loop.create_task(create_sub_wallet(tenant_id=tenant_id))
    return True


@router.get('/{tenant_id}/info')
def get_tenant_info(tenant_id: str):
    tenant = db.get_item(key=tenant_id, dbname=settings.db_name_tenants)
    return tenant

def prepare_headers_from_token(token: str) -> str:
    headers = {
        "Authorization": 'Bearer ' + token
    }
    return headers

def prepare_headers(tenant_id: str) -> str:
    """
    Get the token from the Tenant in DB and returns the prpared headers.
    """
    tenant: Tenant = db.get_item(key=tenant_id, dbname=settings.db_name_tenants)
    return prepare_headers_from_token(token=tenant.token)

async def create_sub_wallet(tenant_id: str):
    """
    
    """
    if not settings.acapy_api:
        print('ACAPY_API not given, not creating sub-wallets')
        return

    tenant: Tenant = db.get_item(key=tenant_id, dbname=settings.db_name_tenants, default=None)
    if tenant:
        if not tenant.wallet_id:
            # create a new wallet
            data = {
                "wallet_name": str(uuid4()),
                "wallet_key": str(uuid4()),
                "wallet_type": "indy"
            }
            # since we are running behind uvicorn or nginx or all inside docker, it can NOT be deteced
            # automatically and needs to be set in env vars
            webhook_url = get_webhook_base_url(tenant_id=tenant_id) + '/agent/webhook'
            data['wallet_webhook_urls'] = [
                webhook_url
            ]
            r = requests.post(settings.acapy_api + '/multitenancy/wallet', json=data)
            j = r.json()
            tenant = Tenant(**j)

            print(f"token: {tenant.token}")

        header = prepare_headers_from_token(token=tenant.token)

        if (tenant.wallet_id) and (not tenant.did):
            # try to create a new did
            data = {
                "method": "sov",
                "options": {
                    "key_type": "ed25519"
                }
            }
            r = requests.post(settings.acapy_api + '/wallet/did/create', json=data, headers=header)
            j = r.json()
            tenant.did = j['result']['did']
            tenant.verkey = j['result']['verkey']
        if (tenant.did) and (not tenant.nym_registered):
            params = {
                "did": tenant.did,
                "verkey": tenant.verkey
            }
            j = requests.post(settings.acapy_api + '/ledger/register-nym', params=params).json() # this execution is on the base wallet - don't set headers!
            if j['success'] == True:
                tenant.nym_registered = True

        if (tenant.nym_registered) and (not tenant.did_published):
            params = {
                "did": tenant.did
            }
            j = requests.post(settings.acapy_api + '/wallet/did/public', params=params, headers=header).json()
            if j['result']['posture'] in ['posted', 'public']:
                tenant.did_published = True
        db.set_item(key=tenant_id, item=tenant, dbname=settings.db_name_tenants)
        print('new tenant:')
        print(tenant.json(indent=4))


@router.post('/{tenant_id}/connect')
def connect_did(tenant_id: str, did_exchange_request: DidExchangeRequest = Body(...)):
    did_exchange_request.use_public_did = 'true' # always!
    params = did_exchange_request.dict()
    r = requests.post(settings.acapy_api + '/didexchange/create-request', params=params, headers=prepare_headers(tenant_id=tenant_id))
    if not r.ok:
        print(r.content)
        return
    
    return r.json()

@router.get('/{tenant_id}/connections')
def get_connections(tenant_id: str):
    r = requests.get(settings.acapy_api + '/connections', headers=prepare_headers(tenant_id=tenant_id))
    j = r.json()
    return j['results']

@router.get('/{tenant_id}/credentials')
def get_credentials(tenant_id: str, include_meta_data: bool = False):
    r = requests.post(settings.acapy_api + '/credentials/w3c', json={}, headers=prepare_headers(tenant_id=tenant_id))
    j = r.json()
    result = []
    for cred in j['results']:
        if include_meta_data:
            result.append(cred)
        else:
            result.append(cred['cred_value'])
    return result

@router.get('/{tenant_id}/credential/{record_id}')
def get_credential(tenant_id: str, record_id: str):
    j = requests.get(settings.acapy_api + '/credential/w3c/' + record_id, headers=prepare_headers(tenant_id=tenant_id)).json()
    return j

def issue_vc(tenant_id: str, vc):
    r = requests.post(settings.acapy_api + '/issue-credential-2.0/send', json=vc, headers=prepare_headers(tenant_id=tenant_id))
    if not r.ok:
        print(r.content)
        return None
    
    return r.json()


def extract_did_identifier(doc: dict) -> str:
    """
    If contains "proof.verificationMethod" it extracts the did from there and deletes the did method prefix
    It remains the identifier part of the DID
    """
    ver_method = doc['proof']['verificationMethod']
    did = ver_method.split('#')[0]
    did_identifier_part = did.split(':')[-1]
    return did_identifier_part


def fetch_verkey(tenant_id: str, did_identifier: str) -> str:
    """
    Loads the verkey from the ledger for a given DID
    """
    params = {
        'did': did_identifier
    }
    j = requests.get(settings.acapy_api + '/ledger/did-verkey', params=params, headers=prepare_headers(tenant_id=tenant_id)).json()
    verkey = j['verkey']

    return verkey

def verify_doc(tenant_id: str, doc: dict, verkey: str) -> bool:
    """
    Uses the acapy API to verify a document.
    verkey: the verkey (public key) of the signature. It needs to be fetched in another way before this call
    """
    input = {
        'doc': doc,
        'verkey': verkey,
    }
    r = requests.post(settings.acapy_api + '/jsonld/verify', json=input, headers=prepare_headers(tenant_id=tenant_id))
    j = r.json()
    return j['valid']

@router.post('/{tenant_id}/verify', tags=['main'])
def verify_vc_or_vp(tenant_id: str, doc: dict = Body(...)):
    """
    Inut is a doc that contains a proof and/or a sub group of "verifiableCredentials" and if so,
    all items in there are verified as well.
    Remark: we check the signature, but not the proofPurpose (and I think the used acapy method also does not do this)
    """
    # VC or VP?
    credentials = doc.get('verifiableCredential', None)
    is_vp = bool(credentials)

    result = {
        'outer_proof_verified': False
    }
    proof_did = extract_did_identifier(doc=doc)
    proof_verkey = fetch_verkey(tenant_id=tenant_id, did_identifier=proof_did)

    outer_proof_verified = verify_doc(tenant_id=tenant_id, doc=doc, verkey=proof_verkey)
    if(outer_proof_verified):
        result['outer_proof_verified'] = True
    
    if credentials:
        # only in case of VP    
        vc_valid = []
        all_vc_valid = True
        for vc in credentials:
            vc_did = extract_did_identifier(vc)
            vc_verkey = fetch_verkey(tenant_id=tenant_id, did_identifier=vc_did)
            vc_verified = verify_doc(tenant_id=tenant_id, doc=vc, verkey=vc_verkey)
            if vc_verified:
                vc_valid.append(True)
            else:
                vc_valid.append(False)
                all_vc_valid = False

        result['inner_proofs_verified'] = vc_valid
        result['all_inner_proofs_verified'] = all_vc_valid
    return result

def prepare_verification_method(did: str):
    return f"did:sov:{did}#key-1" #TODO: hardcoded key itdentifier

def self_sign(tenant_id: str, credential):
    tenant: Tenant = db.get_item(key=tenant_id, dbname=settings.db_name_tenants)
    options = {
        'proofPurpose': "assertionMethod",
        'verificationMethod': prepare_verification_method(tenant.did)
    }
    verkey = tenant.verkey
    doc = {
        'credential': credential,
        'options': options
    }
    data = {
        'doc': doc,
        'verkey': verkey
    }
    r = requests.post(settings.acapy_api + '/jsonld/sign', json=data, headers=prepare_headers(tenant_id=tenant_id))
    if not r.ok:
        print(r.content)
        return None
    j = r.json()
    return j['signed_doc']



def prefix_did(did):
    if not did.startswith('did:sov:'):
        did = 'did:sov:' + did
    return did
