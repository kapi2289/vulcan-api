# -*- coding: utf-8 -*-

from related import StringField, immutable
from uonet_request_signer_hebe import generate_key_pair

from ._utils import default_device_model, get_firebase_token, log
from .model import Serializable


@immutable
class Keystore(Serializable):
    """A keystore containing of:

    - a PEM-encoded X509 certificate signed using SHA-256 with RSA algorithm
    - SHA-1 fingerprint of the certificate, represented
      as lowercase hexadecimal characters
    - a PEM-encoded PKCS#8 RSA 2048 private key

    Additionally, to use with the Vulcan API the keystore contains:

    - a Firebase Cloud Messaging token - to re-use for every request
    - a device name string, also needed for API requests

    :var str ~.certificate: a PEM-encoded certificate
    :var str ~.fingerprint: the certificate's fingerprint
    :var str ~.private_key: a PEM-encoded RSA 2048 private key
    :var str ~.firebase_token: an FCM token
    :var str ~.device_model: a device model string
    """

    certificate: str = StringField(key="Certificate")
    fingerprint: str = StringField(key="Fingerprint")
    private_key: str = StringField(key="PrivateKey")
    firebase_token: str = StringField(key="FirebaseToken")
    device_model: str = StringField(key="DeviceModel")

    @staticmethod
    def create(
        firebase_token: str = None, device_model: str = default_device_model()
    ) -> "Keystore":
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
