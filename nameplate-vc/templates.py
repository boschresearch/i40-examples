# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/IDunion/i40-examples
#
# SPDX-License-Identifier: Apache-2.0


NAMEPLATE_CREDENTIAL_TYPE = "NameplateCredential"
NAMEPLATE_CONTEXT = """
{
    "aio": "https://admin-shell-io.com/ns#",
    "NameplateCredential": "aio:NameplateCredential",
    "ManufacturerName": "aio:ManufacturerName",
    "ManufacturerProductDesignation": "aio:ManufacturerProductDesignation",
    "PhysicalAddress": "aio:PhysicalAddress",
    "CountryCode": "aio:CountryCode",
    "Street": "aio:Street",
    "Zip": "aio:Zip",
    "CityTown": "aio:CityTown",
    "StateCounty": "aio:StateCounty",
    "ManufacturerProductFamily": "aio:ManufacturerProductFamily",
    "SerialNumber": "aio:SerialNumber",
    "BatchNumber": "aio:BatchNumber",
    "ProductCountryOfOrigin": "aio:ProductCountryOfOrigin",
    "YearOfConstruction": "aio:YearOfConstruction"
}
"""
NAMEPLATE_CONTEXT_TMP = """
{
    "aio": "https://admin-shell-io.com/ns#",
    "@type": "aio:Nameplate",
    "NameplateCredential": "aio:NameplateCredential",
    "ManufacturerName": "aio:ManufacturerName",
    "ManufacturerProductDesignation": "aio:ManufacturerProductDesignation",
    "PhysicalAddress": {
        "@type": "aio:PhysicalAddress",
        "CountryCode": "aio:CountryCode",
        "Street": "aio:Street",
        "Zip": "aio:Zip",
        "CityTown": "aio:CityTown",
        "StateCounty": "aio:StateCounty"
    },
    "ManufacturerProductFamily": "aio:ManufacturerProductFamily",
    "SerialNumber": "aio:SerialNumber",
    "BatchNumber": "aio:BatchNumber",
    "ProductCountryOfOrigin": "aio:ProductCountryOfOrigin",
    "YearOfConstruction": "aio:YearOfConstruction",
    "Marking_CE": {
        "@type": "aio:Marking_CE",
        "CEQualificationPresent": "aio:CEQualificationPresent",
        "File": {
            "@type": "aio:File",
            "mimeType": "aio:mimeType",
            "value": "aio:value"
        }
    }
}
"""


ISSUE_VC_TEMPLATE = """
{
    "connection_id": "",
    "filter": {
        "ld_proof": {
            "credential": {
                "@context": [
                    "https://www.w3.org/2018/credentials/v1"
                ],
                "type": [
                    "VerifiableCredential"
                ],
                "issuer": "",
                "issuanceDate": "",
                "credentialSubject": {}
            },
            "options": {
                "proofType": "Ed25519Signature2018"
            }
        }
    }
}
"""
