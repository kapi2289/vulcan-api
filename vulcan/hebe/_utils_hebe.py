# -*- coding: utf-8 -*-

import math, time
from datetime import datetime
import platform
import urllib

from .._utils import (
    uuid,
    get_firebase_token,
    get_base_url,
    log,
    VulcanAPIException,
)

APP_NAME = "DzienniczekPlus 2.0"
APP_VERSION = "1.4.2"
APP_OS = "Android"
APP_USER_AGENT = "Dart/2.10 (dart:io)"


def default_device_model():
    return "Vulcan API (Python {})".format(platform.python_version())


def millis():
    return math.floor(time.time() * 1000)


def now_datetime():  # UTC+0
    return datetime.utcnow()


def now_iso():  # ISO 8601, local timezone
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now_gmt():  # RFC 2822, UTC+0
    return datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")


def urlencode(s):
    return urllib.parse.quote(str(s))
