# -*- coding: utf-8 -*-

import logging
import math
import platform
import time
import urllib
import uuid as _uuid
from datetime import datetime, timezone

import aiohttp

from ._exceptions import InvalidTokenException

APP_NAME = "DzienniczekPlus 2.0"
APP_VERSION = "1.4.2"
APP_OS = "Android"
APP_USER_AGENT = "Dart/2.10 (dart:io)"

log = logging.getLogger("client")
log.setLevel(logging.INFO)

handler = logging.StreamHandler()
log.addHandler(handler)

TIME_FORMAT_H_M = "%H:%M"


def default_device_model():
    return f"Vulcan API (Python {platform.python_version()})"


async def get_base_url(token):
    code = token[:3]
    components = await get_components()
    try:
        return components[code]
    except KeyError as e:
        raise InvalidTokenException() from e


async def get_components():
    log.info("Getting Vulcan components...")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://komponenty.vulcan.net.pl/UonetPlusMobile/RoutingRules.txt"
        ) as r:
            if r.headers["Content-Type"] == "text/plain":
                r_txt = await r.text()
                components = (c.split(",") for c in r_txt.split())
                components = {a[0]: a[1] for a in components}
            else:
                components = {}
            components["FK1"] = "http://api.fakelog.tk"
            return components


async def get_firebase_token():
    async with aiohttp.ClientSession() as session:
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
            "Authorization": f"AidLogin {aid}",
            "User-Agent": "Android-GCM/1.5",
            "app": app,
        }

        async with session.post(
            "https://android.clients.google.com/c2dm/register3",
            data=data,
            headers=headers,
        ) as r:
            r_txt = await r.text()
            return r_txt.split("=")[1]


def millis():
    return math.floor(time.time() * 1000)


def now_datetime():  # RFC 2822, UTC+0
    return datetime.now(timezone.utc)


def now_iso(dt=None):  # ISO 8601, local timezone
    return (dt or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")


def now_gmt(dt=None):  # RFC 2822, UTC+0
    return (dt or datetime.now(timezone.utc)).strftime("%a, %d %b %Y %H:%M:%S GMT")


def uuid(seed=None):
    if seed:
        return str(_uuid.uuid5(_uuid.NAMESPACE_X500, str(seed)))
    return str(_uuid.uuid4())


def urlencode(s):
    return urllib.parse.quote(str(s))
