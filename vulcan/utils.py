# -*- coding: utf-8 -*-

import uuid as _uuid
import time
import math
from OpenSSL import crypto
import json
import base64
import logging
import requests
import pytz
from datetime import datetime


log = logging.getLogger('client')
log.setLevel(logging.INFO)

handler = logging.StreamHandler()
log.addHandler(handler)

tz = pytz.timezone('Europe/Warsaw')

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

def get_components():
    r = requests.get('http://komponenty.vulcan.net.pl/UonetPlusMobile/RoutingRules.txt')
    components = (c.split(',') for c in r.text.split())
    return {a[0]: a[1] for a in components}

def get_base_url(token):
    code = token[0:3]
    components = get_components()
    return components[code]

def timestamp_to_datetime(ts):
    return pytz.utc.localize(datetime.utcfromtimestamp(ts)).astimezone(tz)

def timestamp_to_date(ts):
    return timestamp_to_datetime(ts).date()
