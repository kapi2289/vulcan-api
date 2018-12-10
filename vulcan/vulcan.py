# -*- coding: UTF-8 -*-

from .utils import *
import platform
import requests

class Vulcan(object):

    app_name = 'VULCAN-Android-ModulUcznia'
    app_version = '18.10.1.433'
    cert_passphrase = 'CE75EA598C7743AD9B0B7328DED85B06'

    def __init__(self, cert):
        self._cert = cert
        self._session = requests.session()
        self._headers = {
            'User-Agent': 'MobileUserAgent',
            'RequestCertificateKey': cert['CertyfikatKlucz'],
            'Connection': 'close',
        }
        self._url = cert['AdresBazowyRestApi']
        self._base_url = self._url + 'mobile-api/Uczen.v3.'
        self._full_url = None
        self.user = None

    @staticmethod
    def create(token, symbol, pin):
        data = {
            'PIN': str(pin),
            'TokenKey': token,
            'AppVersion': Vulcan.app_version,
            'DeviceId': uuid(),
            'DeviceName': 'Vulcan API',
            'DeviceNameUser': '',
            'DeviceDescription': '',
            'DeviceSystemType': 'Python',
            'DeviceSystemVersion': platform.python_version(),
            'RemoteMobileTimeKey': now() + 1,
            'TimeKey': now(),
            'RequestId': uuid(),
            'RemoteMobileAppVersion': Vulcan.app_version,
            'RemoteMobileAppName': Vulcan.app_name,
        }
        headers = {
            'RequestMobileType': 'RegisterDevice',
            'User-Agent': 'MobileUserAgent',
        }
        url = 'https://lekcjaplus.vulcan.net.pl/{}/mobile-api/Uczen.v3.UczenStart/Certyfikat'.format(symbol)
        try:
            r = requests.post(url, json=data, headers=headers)
            j = r.json()
            return j['TokenCert']
        except:
            raise VulcanAPIException('Cannot create the certificate!')

    def _payload(self, json):
        payload = {
            'RemoteMobileTimeKey': now() + 1,
            'TimeKey': now(),
            'RequestId': uuid(),
            'RemoteMobileAppVersion': Vulcan.app_version,
            'RemoteMobileAppName': Vulcan.app_name,
        }
        if json:
            payload.update(json)
        return payload

    def _signature(self, json):
        self._headers['RequestSignatureValue'] = signature(self._cert['CertyfikatPfx'], Vulcan.cert_passphrase, json)

    def _request(self, _type, url, params=None, data=None, json=None, as_json=True):
        payload = self._payload(json)
        self._signature(payload)
        if _type == 'GET':
            r = self._session.get(url, params=params, data=data, json=payload, headers=self._headers)
        elif _type == 'POST':
            r = self._session.post(url, params=params, data=data, json=payload, headers=self._headers)
        if as_json:
            try:
                return r.json()
            except:
                raise VulcanAPIException('Bad request')
        return r

    def _get(self, url, params=None, data=None, json=None, as_json=True):
        return self._request(_type='GET', url=url, params=params, data=data, json=json, as_json=as_json)

    def _post(self, url, params=None, data=None, json=None, as_json=True):
        return self._request(_type='POST', url=url, params=params, data=data, json=json, as_json=as_json)
