# -*- coding: utf-8 -*-
import json
import platform

import requests, aiohttp
from related import immutable, StringField, to_json, to_model

from ._utils import uuid, now, get_base_url, log, APP_VERSION, APP_NAME


@immutable
class Certificate:
    pfx = StringField(key="CertyfikatPfx")
    key = StringField(key="CertyfikatKlucz")
    key_formatted = StringField(key="CertyfikatKluczSformatowanyTekst")
    base_url = StringField(key="AdresBazowyRestApi")

    @property
    def json(self):
        return json.loads(to_json(self))

    @classmethod
    async def get(cls, token, symbol, pin):
        token = str(token).upper()
        symbol = str(symbol).lower()
        pin = str(pin)

        data = {
            "PIN": pin,
            "TokenKey": token,
            "AppVersion": APP_VERSION,
            "DeviceId": uuid(),
            "DeviceName": "Vulcan API",
            "DeviceNameUser": "",
            "DeviceDescription": "",
            "DeviceSystemType": "Python",
            "DeviceSystemVersion": platform.python_version(),
            "RemoteMobileTimeKey": now() + 1,
            "TimeKey": now(),
            "RequestId": uuid(),
            "RemoteMobileAppVersion": APP_VERSION,
            "RemoteMobileAppName": APP_NAME,
        }

        headers = {
            "RequestMobileType": "RegisterDevice",
            "User-Agent": "MobileUserAgent",
        }

        base_url = await get_base_url(token)
        url = "{}/{}/mobile-api/Uczen.v3.UczenStart/Certyfikat".format(base_url, symbol)

        log.info("Registering...")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as r:
                j = await r.json()
                log.debug(j)

                cert = j["TokenCert"]
                log.info("Registered successfully!")
                return to_model(cls, cert)
