# -*- coding: utf-8 -*-

import json, io

from related import immutable, StringField

from uonet_request_signer_hebe import generate_key_pair
from ._serializable import Serializable
from ._api import Api

from ._utils_hebe import (
    get_firebase_token,
    log,
    default_device_model,
)


@immutable
class Keystore(Serializable):
    certificate = StringField(key="Certificate")
    fingerprint = StringField(key="Fingerprint")
    private_key = StringField(key="PrivateKey")
    firebase_token = StringField(key="FirebaseToken")
    device_model = StringField(key="DeviceModel")

    @staticmethod
    def create(firebase_token=None, device_model=default_device_model()):
        log.info("Generating key pair...")
        keystore = Keystore(
            *generate_key_pair(),
            firebase_token if firebase_token else get_firebase_token(),
            device_model
        )
        log.info(
            "Generated for {}, sha1: {}".format(device_model, keystore.fingerprint)
        )
        return keystore
