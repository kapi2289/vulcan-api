# -*- coding: utf-8 -*-

import datetime
import logging
import math
import time
import uuid as _uuid
from operator import itemgetter

import pytz
import requests
from uonet_request_signer import sign_content

APP_NAME = "VULCAN-Android-ModulUcznia"
APP_VERSION = "18.10.1.433"

log = logging.getLogger("client")
log.setLevel(logging.INFO)

handler = logging.StreamHandler()
log.addHandler(handler)

tz = pytz.timezone("Europe/Warsaw")

TIME_FORMAT_H_M = "%H:%M"


class VulcanAPIException(Exception):
    pass


def now():
    return math.floor(time.time())


def uuid(seed=None):
    if seed:
        return str(_uuid.uuid5(_uuid.NAMESPACE_X500, str(seed)))
    return str(_uuid.uuid4())


def find(_list, value, key="Id"):
    return next((i for i in _list if i[key] == value), None)


def signature(certificate, data):
    return sign_content(certificate.sign_password, certificate.pfx, data)


def get_components():
    log.info("Getting Vulcan components...")
    r = requests.get("http://komponenty.vulcan.net.pl/UonetPlusMobile/RoutingRules.txt")
    components = (c.split(",") for c in r.text.split())
    components = {a[0]: a[1] for a in components}
    components.update({"FK1": "http://api.fakelog.cf"})
    return components


def get_firebase_token():
    log.info("Getting Firebase token...")
    aid = "4609707972546570896:3626695765779152704"
    device = aid.split(":")[0]
    app = "pl.vulcan.uonetmobile"

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


def get_base_url(token):
    code = token[0:3]
    components = get_components()
    try:
        return components[code]
    except KeyError:
        raise VulcanAPIException("Niepoprawny token!")


def sort_and_filter_dates(
    _list, date_from, date_to, sort_key="Data", date_key="DataTekst"
):
    _list = sorted(_list, key=itemgetter(sort_key))
    return list(
        filter(
            lambda x: date_from
            >= datetime.datetime.strptime(x[date_key], "%Y-%m-%d").date()
            >= date_to,
            _list,
        )
    )


def dict_only(d, keys):
    return {key: d.get(key) for key in d.keys() & set(keys)}
