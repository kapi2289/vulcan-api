# -*- coding: utf-8 -*-

import requests
from related import to_model

from ._certificate import Certificate
from ._dictionaries import Dictionaries
from ._utils import now, uuid, signature, VulcanAPIException, log, APP_NAME, APP_VERSION


class Api:
    def __init__(self, certificate):
        self._session = requests.session()
        self.cert = to_model(Certificate, certificate)
        self.base_url = self.cert.base_url + "mobile-api/Uczen.v3."
        self.full_url = None
        self.dict = None
        self.student = None

    def _payload(self, json):
        payload = {
            "RemoteMobileTimeKey": now() + 1,
            "TimeKey": now(),
            "RequestId": uuid(),
            "RemoteMobileAppVersion": APP_VERSION,
            "RemoteMobileAppName": APP_NAME,
        }

        if self.student:
            payload["IdOkresKlasyfikacyjny"] = self.student.period.id
            payload["IdUczen"] = self.student.id
            payload["IdOddzial"] = self.student.class_.id
            payload["LoginId"] = self.student.login_id

        if json:
            payload.update(json)

        return payload

    def _headers(self, json):
        return {
            "User-Agent": "MobileUserAgent",
            "RequestCertificateKey": self.cert.key,
            "Connection": "close",
            "RequestSignatureValue": signature(self.cert.pfx, json),
        }

    def _request(self, method, endpoint, json=None, as_json=True, **kwargs):
        payload = self._payload(json)
        headers = self._headers(payload)
        url = endpoint if endpoint.startswith("http") else self.full_url + endpoint

        r = self._session.request(method, url, json=payload, headers=headers, **kwargs)

        if as_json:
            try:
                log.debug(r.text)
                return r.json()
            except ValueError:
                raise VulcanAPIException("An unexpected exception occurred.")

        return r

    def get(self, endpoint, json=None, as_json=True, **kwargs):
        return self._request("GET", endpoint, json=json, as_json=as_json, **kwargs)

    def post(self, endpoint, json=None, as_json=True, **kwargs):
        return self._request("POST", endpoint, json=json, as_json=as_json, **kwargs)

    def set_student(self, student):
        self.student = student
        self.full_url = (
            self.cert.base_url + student.school.symbol + "/mobile-api/Uczen.v3."
        )
        self.dict = Dictionaries.get(self)
