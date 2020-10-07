# -*- coding: utf-8 -*-

import json, io

from related import immutable, StringField, to_json, to_model
from uonet_request_signer_hebe import generate_key_pair
from ._api import Api

from ._utils_hebe import (
    uuid,
    get_firebase_token,
    get_base_url,
    log,
    APP_OS,
    default_device_model
)


@immutable
class Keystore:
    certificate = StringField(key="Certificate")
    fingerprint = StringField(key="Fingerprint")
    private_key = StringField(key="PrivateKey")

    @property
    def as_json(self):
        return to_json(self)

    @property
    def as_dict(self):
        return json.loads(self.as_json)

    def __str__(self):
        return self.as_json

    @staticmethod
    def create():
        log.info("Generating key pair...")
        keystore = Keystore(*generate_key_pair())
        log.info("Generated, sha1: " + keystore.fingerprint)
        return keystore

    @classmethod
    def load(cls, data):
        if isinstance(data, dict):
            return to_model(cls, dict)
        elif isinstance(data, io.IOBase):
            return to_model(cls, json.load(data))
        elif isinstance(data, str):
            return to_model(cls, json.loads(data))
        else:
            raise ValueError("Unknown data type")

    def register(self, token, symbol, pin):
        token = str(token).upper()
        symbol = str(symbol).lower()
        pin = str(pin)

        firebase_token = get_firebase_token()
        device_model = default_device_model()

        body = {
            "OS": APP_OS,
            "DeviceModel": device_model,
            "Certificate": self.certificate,
            "CertificateType": "X509",
            "CertificateThumbprint": self.fingerprint,
            "PIN": pin,
            "SecurityToken": token,
            "SelfIdentifier": uuid()
        }

        base_url = get_base_url(token)
        full_url = f"{base_url}/{symbol}/api/mobile/register/new"

        log.info(f"Registering to {symbol}...")

        api = Api(self, firebase_token, device_model)
        log.info(str(
            api.post(full_url, body)
        ))
