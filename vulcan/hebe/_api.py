# -*- coding: utf-8 -*-

import requests

# from ._keystore import Keystore
from uonet_request_signer_hebe import get_signature_values

from ._utils_hebe import (
    uuid,
    millis,
    now_iso,
    now_gmt,
    now_datetime,
    log,
    APP_VERSION,
    APP_NAME,
    APP_OS,
    APP_USER_AGENT,
    default_device_model,
    VulcanAPIException
)


class Api:
    def __init__(self, keystore, firebase_token, device_model=default_device_model()):
        self._session = requests.session()
        # if not isinstance(keystore, Keystore):
        #     raise ValueError("The argument must be a Keystore")
        self.keystore = keystore
        self.firebase_token = firebase_token
        self.device_model = device_model

    def _build_payload(self, envelope):
        return {
            "AppName": APP_NAME,
            "AppVersion": APP_VERSION,
            "CertificateId": self.keystore.fingerprint,
            "Envelope": envelope,
            "FirebaseToken": self.firebase_token,
            "API": 1,
            "RequestId": uuid(),
            "Timestamp": millis(),
            "TimestampFormatted": now_iso()
        }
    
    def _build_headers(self, full_url, payload):
        digest, canonical_url, signature = get_signature_values(
            self.keystore.fingerprint,
            self.keystore.private_key,
            str(payload),
            full_url,
            now_datetime()
        )
        headers = {
            "User-Agent": APP_USER_AGENT,
            "vOS": APP_OS,
            "vDeviceModel": self.device_model,
            "vAPI": "1",
            "vDate": now_gmt(),
            "vCanonicalUrl": canonical_url,
            "Signature": signature
        }
        if digest:
            headers['Digest'] = digest
            headers['Content-Type'] = 'application/json'
        return headers
    
    def _request(self, method, full_url, body=None, **kwargs):
        payload = self._build_payload(body) if body and method == "POST" else None
        headers = self._build_headers(full_url, payload)

        r = self._session.request(method, full_url, data=str(payload), headers=headers, **kwargs)

        try:
            log.debug(r.text)
            return r.json()
        except ValueError:
            raise VulcanAPIException("An unexpected exception occurred.")

    def post(self, full_url, body, **kwargs):
        return self._request("POST", full_url, body, **kwargs)
