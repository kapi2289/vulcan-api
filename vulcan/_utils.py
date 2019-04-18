import logging
import math
import time
import uuid as _uuid
from datetime import datetime
from operator import itemgetter

import pytz
import requests
from uonet_request_signer import sign_content

log = logging.getLogger("client")
log.setLevel(logging.INFO)

handler = logging.StreamHandler()
log.addHandler(handler)

tz = pytz.timezone("Europe/Warsaw")


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
    try:
        return components[code]
    except KeyError:
        raise VulcanAPIException("Niepoprawny token!")


def timestamp_to_datetime(ts):
    return pytz.utc.localize(datetime.utcfromtimestamp(ts)).astimezone(tz)


def timestamp_to_date(ts):
    return timestamp_to_datetime(ts).date()


def concat_hours_and_minutes(date, ts):
    d = timestamp_to_datetime(ts)
    return date.replace(hour=d.hour, minute=d.minute)


def sort_and_filter_date(_list, date):
    _list = sorted(_list, key=itemgetter("Data"))
    return list(filter(lambda x: x["DataTekst"] == date, _list))
