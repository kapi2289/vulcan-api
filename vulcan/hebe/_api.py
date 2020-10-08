# -*- coding: utf-8 -*-

import requests
import json

# from ._keystore import Keystore
from uonet_request_signer_hebe import get_signature_values

from ._utils_hebe import (
    uuid,
    millis,
    now_iso,
    now_gmt,
    now_datetime,
    urlencode,
    log,
    APP_VERSION,
    APP_NAME,
    APP_OS,
    APP_USER_AGENT,
    VulcanAPIException,
)


class Api:
    def __init__(self, keystore, account=None):
        self._session = requests.session()
        # if not isinstance(keystore, Keystore):
        #     raise ValueError("The argument must be a Keystore")
        self.keystore = keystore
        if account:
            self.rest_url = account.rest_url

    def _build_payload(self, envelope: dict) -> dict:
        return {
            "AppName": APP_NAME,
            "AppVersion": APP_VERSION,
            "CertificateId": self.keystore.fingerprint,
            "Envelope": envelope,
            "FirebaseToken": self.keystore.firebase_token,
            "API": 1,
            "RequestId": uuid(),
            "Timestamp": millis(),
            "TimestampFormatted": now_iso(),
        }

    def _build_headers(self, full_url: str, payload: str) -> dict:
        digest, canonical_url, signature = get_signature_values(
            self.keystore.fingerprint,
            self.keystore.private_key,
            payload,
            full_url,
            now_datetime(),
        )

        headers = {
            "User-Agent": APP_USER_AGENT,
            "vOS": APP_OS,
            "vDeviceModel": self.keystore.device_model,
            "vAPI": "1",
            "vDate": now_gmt(),
            "vCanonicalUrl": canonical_url,
            "Signature": signature,
        }

        if digest:
            headers["Digest"] = digest
            headers["Content-Type"] = "application/json"

        return headers

    def _request(self, method: str, url: str, body: dict = None, **kwargs) -> dict:
        full_url = (
            url
            if url.startswith("http")
            else self.rest_url + url
            if self.rest_url
            else None
        )
        if not full_url:
            raise ValueError("Relative URL specified but no account loaded")

        payload = self._build_payload(body) if body and method == "POST" else None
        payload = json.dumps(payload)
        headers = self._build_headers(full_url, payload)

        log.debug(" > {} to {}".format(method, full_url))

        r = self._session.request(
            method, full_url, data=payload, headers=headers, **kwargs
        )

        try:
            response = r.json()
            envelope = response["Envelope"]
            log.debug(" < " + str(envelope))
            return envelope  # TODO error handling
        except ValueError:
            raise VulcanAPIException("An unexpected exception occurred.")

    def get(self, url: str, query: dict = None, **kwargs) -> dict:
        query = (
            "&".join(x + "=" + urlencode(query[x]) for x in query) if query else None
        )
        if query:
            url += "?" + query
        return self._request("GET", url, body=None, **kwargs)

    def post(self, url: str, body: dict, **kwargs) -> dict:
        return self._request("POST", url, body, **kwargs)
