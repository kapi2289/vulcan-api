# -*- coding: utf-8 -*-

from related import IntegerField, StringField, immutable

from ._api import Api
from ._endpoints import DEVICE_REGISTER
from ._keystore import Keystore
from ._utils import APP_OS, get_base_url, log, uuid
from .model import Serializable


@immutable
class Account(Serializable):
    """An account in the e-register.

    :var int ~.login_id: the account's login ID
    :var str ~.user_login: the account's login name (email/username)
    :var str ~.user_name: probably the same as user_login
    :var str ~.rest_url: the API base URL for the partition symbol
    """

    login_id: int = IntegerField(key="LoginId")
    user_login: str = StringField(key="UserLogin")
    user_name: str = StringField(key="UserName")
    rest_url: str = StringField(key="RestURL")

    @staticmethod
    async def register(
        keystore: Keystore, token: str, symbol: str, pin: str
    ) -> "Account":
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

        base_url = await get_base_url(token)
        full_url = "/".join([base_url, symbol, DEVICE_REGISTER])

        log.info("Registering to {}...".format(symbol))

        api = Api(keystore)
        response = await api.post(full_url, body)
        await api.close()

        log.info("Successfully registered as {}".format(response["UserName"]))

        return Account.load(response)
