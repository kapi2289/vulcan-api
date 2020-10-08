# -*- coding: utf-8 -*-

from related import immutable, StringField, IntegerField

from .model._serializable import Serializable
from ._api import Api
from ._keystore import Keystore
from ._endpoints import DEVICE_REGISTER

from ._utils_hebe import (
    uuid,
    get_base_url,
    log,
    APP_OS,
)


@immutable
class Account(Serializable):
    login_id = IntegerField(key="LoginId")
    user_login = StringField(key="UserLogin")
    user_name = StringField(key="UserName")
    rest_url = StringField(key="RestURL")

    @staticmethod
    def register(keystore: Keystore, token: str, symbol: str, pin: str) -> "Account":
        token = str(token).upper()
        symbol = str(symbol).lower()
        pin = str(pin)

        body = {
            "OS": APP_OS,
            "DeviceModel": keystore.device_model,
            "Certificate": keystore.certificate,
            "CertificateType": "X509",
            "CertificateThumbprint": keystore.fingerprint,
            "PIN": pin,
            "SecurityToken": token,
            "SelfIdentifier": uuid(keystore.fingerprint),
        }

        base_url = get_base_url(token)
        full_url = "/".join([base_url, symbol, DEVICE_REGISTER])

        log.info("Registering to {}...".format(symbol))

        api = Api(keystore)
        response = api.post(full_url, body)

        return Account.load(response)
