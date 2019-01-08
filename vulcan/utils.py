# -*- coding: utf-8 -*-

import uuid as _uuid
import time
import math
from OpenSSL import crypto
import json
import base64
import logging


log = logging.getLogger(__name__)

class VulcanAPIException(Exception):
    pass

def now():
    return math.floor(time.time())

def uuid():
    return str(_uuid.uuid4())

def find(_list, key, value):
    return next((i for i in _list if i[key] == value), None)

def signature(cert, passphrase, data):
    p12 = crypto.load_pkcs12(base64.b64decode(cert), passphrase.encode('utf-8'))
    sign = crypto.sign(p12.get_privatekey(), json.dumps(data).encode('utf-8'), 'RSA-SHA1')
    return base64.b64encode(sign).decode('utf-8')
