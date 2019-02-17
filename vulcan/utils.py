# -*- coding: utf-8 -*-

import uuid as _uuid
import time
import math
from uonet_request_signer import sign_content
import json
import base64
import logging
import requests


log = logging.getLogger("client")
log.setLevel(logging.INFO)

handler = logging.StreamHandler()
log.addHandler(handler)


class VulcanAPIException(Exception):
    pass


def now():
    return math.floor(time.time())


def uuid():
    return str(_uuid.uuid4())


def find(_list, key, value):
    return next((i for i in _list if i[key] == value), None)


def signature(cert, data):
    return sign_content("CE75EA598C7743AD9B0B7328DED85B06", cert, data)


def get_components():
    r = requests.get("http://komponenty.vulcan.net.pl/UonetPlusMobile/RoutingRules.txt")
    components = (c.split(",") for c in r.text.split())
    return {a[0]: a[1] for a in components}


def get_base_url(token):
    code = token[0:3]
    components = get_components()
    return components[code]
