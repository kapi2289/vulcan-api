# -*- coding: UTF-8 -*-

import uuid as _uuid
import time
import math

class VulcanAPIException(Exception):
    pass

def now():
    return math.floor(time.time())

def uuid():
    return str(_uuid.uuid4())

def find(_list, key, value):
    return next(i for i in _list if i[key] == value)
