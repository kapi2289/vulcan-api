# -*- coding: utf-8 -*-

import logging
import math
import platform
import time
import urllib
import uuid as _uuid
from datetime import datetime

import requests

APP_NAME = "DzienniczekPlus 2.0"
APP_VERSION = "1.4.2"
APP_OS = "Android"
APP_USER_AGENT = "Dart/2.10 (dart:io)"

log = logging.getLogger("client")
log.setLevel(logging.INFO)

handler = logging.StreamHandler()
log.addHandler(handler)

TIME_FORMAT_H_M = "%H:%M"


class VulcanAPIException(Exception):
    pass


def default_device_model():
    return "Vulcan API (Python {})".format(platform.python_version())


def get_base_url(token):
    code = token[0:3]
    components = get_components()
    try:
        return components[code]
    except KeyError:
        raise VulcanAPIException("Niepoprawny token!")


def get_components():
    log.info("Getting Vulcan components...")
    r = requests.get("http://komponenty.vulcan.net.pl/UonetPlusMobile/RoutingRules.txt")
    if r.headers["Content-Type"] == "text/plain":
        components = (c.split(",") for c in r.text.split())
        components = {a[0]: a[1] for a in components}
    else:
        components = {}
    components.update({"FK1": "http://api.fakelog.cf"})
    return components


def get_firebase_token():
    log.info("Getting Firebase token...")
    aid = "4609707972546570896:3626695765779152704"
    device = aid.split(":")[0]
    app = "pl.edu.vulcan.hebe"

    data = {
        "sender": "987828170337",
        "X-scope": "*",
        "X-gmp_app_id": "1:987828170337:android:ac97431a0a4578c3",
        "app": app,
        "device": device,
    }

    headers = {
        "Authorization": "AidLogin {}".format(aid),
        "User-Agent": "Android-GCM/1.5",
        "app": app,
    }

    r = requests.post(
        "https://android.clients.google.com/c2dm/register3", data=data, headers=headers
    )
    token = r.text.split("=")[1]

    return token


def millis():
    return math.floor(time.time() * 1000)


def now_datetime():  # UTC+0
    return datetime.utcnow()


def now_iso(dt=None):  # ISO 8601, local timezone
    return (dt or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")


def now_gmt(dt=None):  # RFC 2822, UTC+0
    return (dt or datetime.utcnow()).strftime("%a, %d %b %Y %H:%M:%S GMT")


def uuid(seed=None):
    if seed:
        return str(_uuid.uuid5(_uuid.NAMESPACE_X500, str(seed)))
    return str(_uuid.uuid4())


def urlencode(s):
    return urllib.parse.quote(str(s))
