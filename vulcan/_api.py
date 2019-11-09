import requests

from ._utils import now, uuid, signature, VulcanAPIException, log


class Api:
    APP_NAME = "VULCAN-Android-ModulUcznia"
    APP_VERSION = "18.10.1.433"

    def __init__(self, certificate):
        self._session = requests.session()
        self._cert = certificate
        self._url = certificate["AdresBazowyRestApi"]
        self._base_url = self._url + "mobile-api/Uczen.v3."
        self._full_url = None
        self.student = None

    def _payload(self, json):
        payload = {
            "RemoteMobileTimeKey": now() + 1,
            "TimeKey": now(),
            "RequestId": uuid(),
            "RemoteMobileAppVersion": Api.APP_VERSION,
            "RemoteMobileAppName": Api.APP_NAME,
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
            "RequestCertificateKey": self._cert["CertyfikatKlucz"],
            "Connection": "close",
            "RequestSignatureValue": signature(self._cert["CertyfikatPfx"], json),
        }

    def _request(self, method, endpoint, json=None, as_json=True, **kwargs):
        payload = self._payload(json)
        headers = self._headers(payload)
        url = endpoint if endpoint.startswith("http") else self._full_url + endpoint

        r = self._session.request(method, url, json=payload, headers=headers, **kwargs)

        if as_json:
            try:
                log.debug(r.text)
                return r.json()
            except ValueError:
                raise VulcanAPIException("An unexpected exception occurred.")

        return r

    def _get(self, endpoint, json=None, as_json=True, **kwargs):
        return self._request("GET", endpoint, json=json, as_json=as_json, **kwargs)

    def _post(self, endpoint, json=None, as_json=True, **kwargs):
        return self._request("POST", endpoint, json=json, as_json=as_json, **kwargs)
