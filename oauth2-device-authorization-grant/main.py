"""
 Copyright (c) 2021 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/IDunion/i40-examples

 SPDX-License-Identifier: Apache-2.0
"""

import requests
import json
import time
import webbrowser
import jwt
import os

BASE_URL = os.environ.get('BASE_URL') or 'http://localhost:8080'
CLIENT_ID = os.environ.get('CLIENT_ID') or 'devicegrant'
REALM = os.environ.get('REALM') or 'test'
DISABLE_SSL_VERIFY = os.environ.get('DISABLE_SSL_VERIFY', 'False').lower() in ('true', '1')

DEVICE_GRANT_ENDPOINT = os.environ.get('DEVICE_GRANT_ENDPOINT') or BASE_URL + '/auth/realms/' + REALM + '/protocol/openid-connect/auth/device'
TOKEN_ENDPOINT = os.environ.get('TOKEN_ENDPOINT') or BASE_URL + '/auth/realms/' + REALM + '/protocol/openid-connect/token'
USERINFO_ENDPOINT = BASE_URL + '/auth/realms/' + REALM + '/protocol/openid-connect/userinfo'
CERTIFICATE_ENDPOINT = BASE_URL + '/auth/realms/' + REALM + '/protocol/openid-connect/certs'

def pprint(j):
    print(json.dumps(j, indent=4))

session = requests.Session()
if DISABLE_SSL_VERIFY:
    session.verify = False

r = session.post(DEVICE_GRANT_ENDPOINT, {'client_id': CLIENT_ID})
rj = r.json()
device_grant_result = rj
device_code = rj['device_code']
interval = rj['interval']
pprint(rj)

try:
    time.sleep(3)
    #webbrowser.open_new_tab(device_grant_result['verification_uri_complete'])
except:
    print('Could not open browser, please try it manually')

print('Use this URL to signin: ', device_grant_result['verification_uri_complete'])
print('Polling authentication state...')
token_result = None
while True:
    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id': CLIENT_ID,
        'device_code': device_code
    }
    r = session.post(TOKEN_ENDPOINT, data)
    rj = r.json()
    if 'error' in rj:
        #pprint(rj)
        #print('Server Reply: ', rj['error'])
        #print('Server Reply: ', rj['error_description'])
        #print('Use this URL to signin: ', device_grant_result['verification_uri_complete'])
        time.sleep(interval)
    else:
        token_result = rj
        break

pprint(token_result)

r = session.post(USERINFO_ENDPOINT, {'access_token': token_result['access_token']})
userinfo = r.json()
print()
at = jwt.decode(token_result['access_token'], options={"verify_signature": False})
print('====== Access Token =====')
pprint(at)
print()

try:
    # try gathering some infomration about the signature of the token
    # this is pure information and not necessary at this point
    # in the i40 example, the aasx server knows all the certificates it trusts
    # (mainly because it might not have an internet connection)
    headers = jwt.api_jws.get_unverified_header(token_result['access_token'])
    print(headers)
    pprint(headers)

    jwks_client = jwt.jwks_client.PyJWKClient(CERTIFICATE_ENDPOINT)
    signing_key = jwks_client.get_signing_key_from_jwt(token_result['access_token'])
    print(signing_key)

    x5c = signing_key._jwk_data.get('x5c')[0]
    print(x5c)
    from OpenSSL.crypto import load_certificate, FILETYPE_PEM, FILETYPE_ASN1
    import base64
    cert = load_certificate(FILETYPE_ASN1, base64.b64decode(x5c))
    cert_sha = cert.digest('sha256').decode()
    print(cert)
    print('x509 serial number: ', cert.get_serial_number())
    print('x509 subject: ', cert.get_subject().get_components())
    print('x509 fingerprint (sha256): ', cert_sha)
except:
    print('Could not gather signature information, e.g. x509 certificate chain.')

print('====== Userinfo =========')
pprint(userinfo)

