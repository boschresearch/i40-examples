# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/IDunion/i40-examples
#
# SPDX-License-Identifier: Apache-2.0

from pydantic import BaseModel, Field
from typing import Union, Optional, Callable, Any, List


class MyBaseModel(BaseModel):
    """
    The customized BaseModel allows to:
    - serialize with camelCase and use Python snake notation internally
    """
    def json(self, *, include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None, exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None, by_alias: bool = False, skip_defaults: bool = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, encoder: Optional[Callable[[Any], Any]] = None, models_as_dict: bool = True, **dumps_kwargs: Any) -> str:
        by_alias = True
        exclude_unset = True
        return super().json(include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, encoder=encoder, models_as_dict=models_as_dict, **dumps_kwargs)

    def dict(self, *, include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None, exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None, by_alias: bool = False, skip_defaults: bool = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False) -> 'DictStrAny':
        by_alias = True
        exclude_unset = True
        return super().dict(include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none)

    class Config:
        allow_population_by_field_name = True

class Tenant(MyBaseModel):
    wallet_id: str = Field(default='')
    wallet_name: str = Field(default='')
    wallet_key: str = Field(default='')
    token: str = Field(default='')
    did: str = Field(default='')
    verkey: str = Field(default='')
    nym_registered: bool = False
    did_published: bool = False
    connections: List[Any] = Field(default=[])

class PhysicalAddress(MyBaseModel):
    country_code: str = Field(default='', alias='CountryCode')
    street: str = Field(default='', alias='Street')
    zip: str = Field(default='', alias='Zip')
    city_town: str = Field(default='', alias='CityTown')
    state_county: str = Field(default='', alias='StateCounty')

class Nameplate(MyBaseModel):
    manufacturer_name: str = Field(default='', alias='ManufacturerName')
    manufacturer_product_designation: str = Field(default='', alias='ManufacturerProductDesignation')
    physical_address: PhysicalAddress = Field(default=None, alias='PhysicalAddress')
    manufacturer_product_family: str = Field(default='', alias='ManufacturerProductFamily')
    serial_number: str = Field(default='', alias='SerialNumber')
    batch_number: str = Field(default='', alias='BatchNumber')
    product_country_of_origin: str = Field(default='', alias='ProductCountryOfOrigin')
    year_of_construction: str = Field(default='', alias='YearOfConstruction')

class DidExchangeRequest(MyBaseModel):
    their_public_did: str
    alias: str
    use_public_did: str = 'true'
