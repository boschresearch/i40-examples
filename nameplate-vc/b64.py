# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/IDunion/i40-examples
#
# SPDX-License-Identifier: Apache-2.0

import base64
import sys

def encode(data: str):
    """
    No padding "=="
    """
    b64_str = base64.urlsafe_b64encode(data.encode())
    b64_str = b64_str.replace(b"=", b"")
    return b64_str.decode()

def decode(b64_data: str):
    b64_data = b64_data + '====' # too many paddings will be ignored anyway...
    result = base64.urlsafe_b64decode(b64_data).decode()
    return result


if __name__ == '__main__':
    """
    First argument will be b64 encoded (without pading).
    This is how i40 registry uses encoded aas IDs in its API
    """
    data = sys.argv[1]
    print(data)
    e = encode(data=data)
    print(e)
