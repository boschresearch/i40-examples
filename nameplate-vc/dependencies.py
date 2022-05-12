# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/IDunion/i40-examples
#
# SPDX-License-Identifier: Apache-2.0

import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    acapy_api: str = 'http://acapy:30000'
    dt_twin_registry: str = ''
    acapy_webhook_base_url: str = ''
    db_name_tenants: str = 'tenants.db'
    db_name_credentials: str = 'credentials.db'
    registry_base_url: str = 'https://registry.h2894164.stratoserver.net'
    endpoint_base_url: str = 'http://localhost:8080'

    class Config:
        env_file = os.getenv('ENV_FILE', '.env')

settings: Settings = Settings()
print(settings.json(indent=4))

DB_KEY_PREFIX_VC = 'VC_'
DB_KEY_PREFIX_VP = 'VP_'

SEMANTIC_ID_VALUES = [
    'https://admin-shell.io/zvei/nameplate/1/0/Nameplate',
    'https://admin-shell.io/zvei/nameplate/1/0/Nameplate',
    'http://admin-shell.io/Nameplate',
    'https://www.hsu-hh.de/aut/aas/nameplate'
]

def get_webhook_base_url(tenant_id: str) -> str:
    return settings.acapy_webhook_base_url + '/' + tenant_id
