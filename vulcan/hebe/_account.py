# -*- coding: utf-8 -*-

from related import immutable, StringField, IntegerField

from ._serializable import Serializable
from ._api import Api

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
    def register(keystore, token, symbol, pin):
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
        full_url = "{}/{}/api/mobile/register/new".format(base_url, symbol)

        log.info("Registering to {}...".format(symbol))

        api = Api(keystore)
        response = api.post(full_url, body)

        return Account.load(response)
