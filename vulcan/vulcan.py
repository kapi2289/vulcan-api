# -*- coding: UTF-8 -*-

from .utils import *
import platform
import requests

class Vulcan(object):

    app_name = 'VULCAN-Android-ModulUcznia'
    app_version = '18.10.1.433'

    def __init__(self, cert):
        pass

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
