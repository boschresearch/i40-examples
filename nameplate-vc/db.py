# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/IDunion/i40-examples
#
# SPDX-License-Identifier: Apache-2.0

import shelve

def get_item(key: str, dbname: str, default = None):
    try:
        with shelve.open(dbname, 'r') as db:
            return db[key]
    except:
        pass
    return default

def set_item(key: str, item, dbname: str):
    try:
        with shelve.open(dbname) as db:
            db[key] = item
            return True
    except:
        pass
    return False

def key_in_db(key: str, dbname: str):
    with shelve.open(dbname) as db:
        return key in db

def get_keys(dbname: str):
    try:
        with shelve.open(dbname, 'r') as db:
            return list(db)
    except:
        pass
    return []

def delete_item(key: str, dbname: str):
    """
    Delete item from db.
    False in case of an error (also non existing item) otherwise True
    """
    try:
        with shelve.open(dbname) as db:
            del db[key]
    except:
        return False
    return True

def delete_all(dbname: str):
    keys = get_keys(dbname=dbname)
    for key in keys:
        delete_item(key=key, dbname=dbname)
