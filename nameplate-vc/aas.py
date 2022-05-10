
# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/IDunion/i40-examples
#
# SPDX-License-Identifier: Apache-2.0

from typing import List
import requests
from dependencies import SEMANTIC_ID_VALUES, settings
import b64

def convert_from_submodel_by_value_to_plain(key_value: list) -> dict:
    """
    Convert from the structure where every key/value pair is a separate object
    into a simpler, plain key/value structure
    """
    result = {}
    for item in key_value:
        for key, value in item.items():
            result[key] = value
    return result

def get_nameplate_endpoint(submodel_endpoints: List):
    try:
        for endpoint in submodel_endpoints:
            semantic_id_value = endpoint['semanticId']['value'][0]
            if semantic_id_value in SEMANTIC_ID_VALUES:
                return endpoint['endpoints'][0]['protocolInformation']['endpointAddress'] #TODO: hardcoded: first element for this semanticId. Why is this a list again?
    except:
        pass
    return None

def get_nameplate_from_registry(aas_id: str, registry_base_url: str):
    """
    Returns the already flattened structure of th nameplate endpoint content or None
    """
    aas_id_b64 = b64.encode(aas_id)
    url = f"{registry_base_url}/registry/shell-descriptors/{aas_id_b64}"
    r = requests.get(url, headers={"accept": "text/plain"})
    if not r.ok:
        print(r.content)
        return None
    j = r.json()
    endpoints = j[0]['submodelDescriptors'] #why the hack is this a list if we provide an identifier???
    nameplate_endpoint = get_nameplate_endpoint(endpoints)
    if not nameplate_endpoint:
        print(f"Could not find Nameplate endpoint aas_id: {aas_id}")
        return None
    
    params = {
        'content': 'value',
    }
    r = requests.get(nameplate_endpoint, params=params)
    if not r.ok:
        print(r.content)
        return None
    j = r.json()
    #plain_nameplate = convert_from_submodel_by_value_to_plain(j)
    return j


