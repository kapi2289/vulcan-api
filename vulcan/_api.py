# -*- coding: utf-8 -*-

import json
from typing import Union

import aiohttp
from uonet_request_signer_hebe import get_signature_values
from yarl import URL

from ._api_helper import ApiHelper
from ._keystore import Keystore
from ._utils import (
    APP_NAME,
    APP_OS,
    APP_USER_AGENT,
    APP_VERSION,
    VulcanAPIException,
    log,
    millis,
    now_datetime,
    now_gmt,
    now_iso,
    urlencode,
    uuid,
)
from .model import Period, Student


class Api:
    """The API service class.

    Provides methods for sending GET/POST requests on a higher
    level, automatically generating the required headers
    and other values.

    :var `~vulcan._api_helper.ApiHelper` ~.helper: a wrapper for getting
         most data objects more easily
    """

    def __init__(self, keystore: Keystore, account=None):
        self._session = aiohttp.ClientSession()
        # if not isinstance(keystore, Keystore):
        #     raise ValueError("The argument must be a Keystore")
        self._keystore = keystore
        if account:
            self._account = account
            self._rest_url = account.rest_url
        self._student = None
        self._period = None
        self.helper = ApiHelper(self)

    def _build_payload(self, envelope: dict) -> dict:
        return {
            "AppName": APP_NAME,
            "AppVersion": APP_VERSION,
            "CertificateId": self._keystore.fingerprint,
            "Envelope": envelope,
            "FirebaseToken": self._keystore.firebase_token,
            "API": 1,
            "RequestId": uuid(),
            "Timestamp": millis(),
            "TimestampFormatted": now_iso(),
        }

    def _build_headers(self, full_url: str, payload: str) -> dict:
        dt = now_datetime()
        digest, canonical_url, signature = get_signature_values(
            self._keystore.fingerprint,
            self._keystore.private_key,
            payload,
            full_url,
            dt,
        )

        headers = {
            "User-Agent": APP_USER_AGENT,
            "vOS": APP_OS,
            "vDeviceModel": self._keystore.device_model,
            "vAPI": "1",
            "vDate": now_gmt(dt),
            "vCanonicalUrl": canonical_url,
            "Signature": signature,
        }

        if digest:
            headers["Digest"] = digest
            headers["Content-Type"] = "application/json"

        return headers

    async def _request(
        self, method: str, url: str, body: dict = None, **kwargs
    ) -> Union[dict, list]:
        if self._session.closed:
            raise RuntimeError("The AioHttp session is already closed.")

        full_url = (
            url
            if url.startswith("http")
            else self._rest_url + url
            if self._rest_url
            else None
        )
        if not full_url:
            raise ValueError("Relative URL specified but no account loaded")

        payload = self._build_payload(body) if body and method == "POST" else None
        payload = json.dumps(payload) if payload else None
        headers = self._build_headers(full_url, payload)

        log.debug(" > {} to {}".format(method, full_url))

        # a workaround for aiohttp incorrectly re-encoding the full URL
        full_url = URL(full_url, encoded=True)

        async with self._session.request(
            method, full_url, data=payload, headers=headers, **kwargs
        ) as r:
            try:
                response = await r.json()
                status = response["Status"]
                envelope = response["Envelope"]

                if status["Code"] == 108:
                    log.debug(" ! " + str(status))
                    raise VulcanAPIException("The certificate is not authorized.")

                elif status["Code"] == 200:
                    log.debug(" ! " + str(status))
                    raise VulcanAPIException("Invalid token.")

                elif status["Code"] == 203:
                    log.debug(" ! " + str(status))
                    raise VulcanAPIException("Invalid PIN.")

                elif status["Code"] == 204:
                    log.debug(" ! " + str(status))
                    raise VulcanAPIException("Expired token.")

                elif status["Code"] != 0:
                    log.debug(" ! " + str(status))
                    raise RuntimeError(status["Message"])

                log.debug(" < " + str(envelope))
                return envelope  # TODO better error handling
            except ValueError:
                raise VulcanAPIException("An unexpected exception occurred.")

    async def get(self, url: str, query: dict = None, **kwargs) -> Union[dict, list]:
        query = (
            "&".join(x + "=" + urlencode(query[x]) for x in query) if query else None
        )
        if query:
            url += "?" + query
        return await self._request("GET", url, body=None, **kwargs)

    async def post(self, url: str, body: dict, **kwargs) -> Union[dict, list]:
        return await self._request("POST", url, body, **kwargs)

    async def open(self):
        if self._session.closed:
            self._session = aiohttp.ClientSession()

    async def close(self):
        await self._session.close()

    @property
    def account(self):
        return self._account

    @property
    def student(self) -> Student:
        return self._student

    @student.setter
    def student(self, student: Student):
        if not self._account:
            raise AttributeError("Load an Account first!")
        self._rest_url = self._account.rest_url + student.unit.code + "/"
        self._student = student
        self.period = student.current_period

    @property
    def period(self) -> Period:
        return self._period

    @period.setter
    def period(self, period: Period):
        self._period = period
