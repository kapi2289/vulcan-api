# -*- coding: utf-8 -*-
import json
import platform

import requests
from related import immutable, StringField, to_json, to_model

from ._utils import (
    uuid,
    now,
    get_firebase_token,
    get_base_url,
    log,
    APP_VERSION,
    APP_NAME,
)


@immutable
class Certificate:
    """Certificate for API request signing

    :param str pfx: PKCS#12 PEM-encoded keystore, containing the signing key pair
    :param str key: Uppercase hexadecimal representation of the certificate's SHA1 fingerprint
    :param str key_formatted: Same as `key`, except the octets are divided by dashes (-)
    :param str base_url: URL base of the API
    """

    pfx = StringField(key="CertyfikatPfx")
    key = StringField(key="CertyfikatKlucz")
    key_formatted = StringField(key="CertyfikatKluczSformatowanyTekst")
    base_url = StringField(key="AdresBazowyRestApi")

    @property
    def json(self):
        return json.loads(to_json(self))

    @property
    def is_fake(self):
        return "fakelog" in self.base_url

    @property
    def sign_password(self):
        return (
            "012345678901234567890123456789AB"
            if self.is_fake
            else "CE75EA598C7743AD9B0B7328DED85B06"
        )

    def __str__(self):
        return str(self.json)

    @classmethod
    def get(cls, token, symbol, pin, name):
        token = str(token).upper()
        symbol = str(symbol).lower()
        pin = str(pin)

        firebase_token = get_firebase_token()

        data = {
            "PIN": pin,
            "TokenKey": token,
            "AppVersion": APP_VERSION,
            "DeviceId": uuid(),
            "DeviceName": name,
            "DeviceNameUser": "",
            "DeviceDescription": "",
            "DeviceSystemType": "Python",
            "DeviceSystemVersion": platform.python_version(),
            "RemoteMobileTimeKey": now() + 1,
            "TimeKey": now(),
            "RequestId": uuid(),
            "RemoteMobileAppVersion": APP_VERSION,
            "RemoteMobileAppName": APP_NAME,
            "FirebaseTokenKey": firebase_token,
        }

        headers = {
            "RequestMobileType": "RegisterDevice",
            "User-Agent": "MobileUserAgent",
        }

        base_url = get_base_url(token)
        url = "{}/{}/mobile-api/Uczen.v3.UczenStart/Certyfikat".format(base_url, symbol)

        log.info("Registering...")

        r = requests.post(url, json=data, headers=headers)
        j = r.json()
        log.debug(j)

        cert = j["TokenCert"]
        log.info("Registered successfully!")

        return to_model(cls, cert)
