# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import platform
from operator import itemgetter

from .models import *


class Vulcan(object):
    """
    Loguje się do dzienniczka za pomocą wygenerowanego certyfikatu

    Args:
        certyfikat (:class:`dict`): Certyfikat wygenerowany za pomocą :func:`vulcan.Vulcan.zarejestruj`
    """

    app_name = "VULCAN-Android-ModulUcznia"
    app_version = "18.10.1.433"

    def __init__(self, certyfikat, logging_level=None):
        self._cert = certyfikat
        self._session = requests.session()
        self._headers = {
            "User-Agent": "MobileUserAgent",
            "RequestCertificateKey": certyfikat["CertyfikatKlucz"],
            "Connection": "close",
        }
        self._url = certyfikat["AdresBazowyRestApi"]
        self._base_url = self._url + "mobile-api/Uczen.v3."
        self._full_url = None

        if logging_level:
            Vulcan.set_logging_level(logging_level)

        self.uczen = None
        uczniowie = self.uczniowie()
        self.ustaw_ucznia(uczniowie[0])

    """
    Ustawia poziom logowania

    Args:
        logging_level (:class:`int`): Poziom logowania z modułu :module:`logging`
    """

    @staticmethod
    def set_logging_level(logging_level):
        log.setLevel(logging_level)

    @staticmethod
    def zarejestruj(token, symbol, pin):
        """
        Rejestruje API jako nowe urządzenie mobilne

        Args:
            token (:class:`str`): Token
            symbol (:class:`str`): Symbol/Nazwa instancji
            pin (:class:`str`): Kod PIN

        Returns:
            :class:`dict`: Certyfikat
        """
        token = str(token).upper()
        symbol = str(symbol).lower()
        pin = str(pin)
        data = {
            "PIN": pin,
            "TokenKey": token,
            "AppVersion": Vulcan.app_version,
            "DeviceId": uuid(),
            "DeviceName": "Vulcan API",
            "DeviceNameUser": "",
            "DeviceDescription": "",
            "DeviceSystemType": "Python",
            "DeviceSystemVersion": platform.python_version(),
            "RemoteMobileTimeKey": now() + 1,
            "TimeKey": now(),
            "RequestId": uuid(),
            "RemoteMobileAppVersion": Vulcan.app_version,
            "RemoteMobileAppName": Vulcan.app_name,
        }
        headers = {
            "RequestMobileType": "RegisterDevice",
            "User-Agent": "MobileUserAgent",
        }
        try:
            base_url = get_base_url(token)
        except KeyError:
            raise VulcanAPIException("Niepoprawny token!")
        url = "{}/{}/mobile-api/Uczen.v3.UczenStart/Certyfikat".format(base_url, symbol)
        log.info("Rejestrowanie...")
        try:
            r = requests.post(url, json=data, headers=headers)
            j = r.json()
            log.debug(j)
            cert = j["TokenCert"]
            assert cert
            log.info("Zarejestrowano pomyślnie!")
            return cert
        except:
            raise VulcanAPIException("Nie można utworzyć certyfikatu!")

    def _payload(self, json):
        payload = {
            "RemoteMobileTimeKey": now() + 1,
            "TimeKey": now(),
            "RequestId": uuid(),
            "RemoteMobileAppVersion": Vulcan.app_version,
            "RemoteMobileAppName": Vulcan.app_name,
        }
        if self.uczen:
            payload["IdOkresKlasyfikacyjny"] = self.uczen.okres.id
            payload["IdUczen"] = self.uczen.id
            payload["IdOddzial"] = self.uczen.klasa.id
            payload["LoginId"] = self.uczen.login_id
        if json:
            payload.update(json)
        return payload

    def _signature(self, json):
        self._headers["RequestSignatureValue"] = signature(
            self._cert["CertyfikatPfx"], json
        )

    def _request(self, _type, url, params=None, data=None, json=None, as_json=True):
        payload = self._payload(json)
        self._signature(payload)
        if _type == "GET":
            r = self._session.get(
                url, params=params, data=data, json=payload, headers=self._headers
            )
        elif _type == "POST":
            r = self._session.post(
                url, params=params, data=data, json=payload, headers=self._headers
            )
        if as_json:
            try:
                return r.json()
            except:
                raise VulcanAPIException("Wystąpił błąd.")
        return r

    def _get(self, url, params=None, data=None, json=None, as_json=True):
        return self._request(
            _type="GET", url=url, params=params, data=data, json=json, as_json=as_json
        )

    def _post(self, url, params=None, data=None, json=None, as_json=True):
        return self._request(
            _type="POST", url=url, params=params, data=data, json=json, as_json=as_json
        )

    def _get_dict(self):
        j = self._post(self._full_url + "Uczen/Slowniki")
        return j["Data"]

    def uczniowie(self):
        """
        Zwraca listę wszystkich uczniów należących do użytkownika

        Returns:
            :class:`list`: Listę uczniów
        """
        j = self._post(self._base_url + "UczenStart/ListaUczniow")
        return list(map(lambda x: Uczen.from_json(x), j["Data"]))

    def ustaw_ucznia(self, uczen):
        """
        Ustawia domyślnego ucznia

        Args:
            uczen (:class:`vulcan.models.Uczen`): Jeden z uczniów zwróconych przez :func:`vulcan.Vulcan.uczniowie`
        """
        self.uczen = uczen
        self._full_url = self._url + uczen.szkola.symbol + "/mobile-api/Uczen.v3."
        self._dict = self._get_dict()

    def plan_lekcji(self, dzien=None):
        """
        Pobiera plan lekcji z danego dnia

        Args:
            dzien (:class:`datetime.date` or :class:`datetime.datetime`): Dzień z którego pobrać plan
                lekcji, jeśli puste pobiera z aktualnego dnia

        Returns:
            :class:`list`: Listę lekcji
        """
        if not dzien:
            dzien = datetime.now()
        dzien_str = dzien.strftime("%Y-%m-%d")
        data = {"DataPoczatkowa": dzien_str, "DataKoncowa": dzien_str}
        j = self._post(self._full_url + "Uczen/PlanLekcjiZeZmianami", json=data)
        plan_lekcji = sorted(j["Data"], key=itemgetter("NumerLekcji"))
        plan_lekcji = list(filter(lambda x: x["DzienTekst"] == dzien_str, plan_lekcji))
        for lekcja in plan_lekcji:
            lekcja["DzienObjekt"] = datetime.fromtimestamp(lekcja["Dzien"]).date()
            lekcja["PoraLekcji"] = find(
                self._dict["PoryLekcji"], "Id", lekcja["IdPoraLekcji"]
            )
            lekcja["Przedmiot"] = find(
                self._dict["Przedmioty"], "Id", lekcja["IdPrzedmiot"]
            )
            lekcja["Pracownik"] = find(
                self._dict["Pracownicy"], "Id", lekcja["IdPracownik"]
            )
            lekcja["PracownikWspomagajacy"] = find(
                self._dict["Pracownicy"], "Id", lekcja["IdPracownikWspomagajacy"]
            )
        return list(map(lambda x: Lekcja.from_json(x), plan_lekcji))

    def sprawdziany(self, dzien=None):
        """
        Pobiera sprawdziany z danego dnia

        Args:
            dzien (:class:`datetime.date` or :class:`datetime.datetime`): Dzień z którego pobrać
                sprawdziany, jeśli puste pobiera z aktualnego dnia

        Returns:
            :class:`list`: Listę sprawdzianów
        """
        if not dzien:
            dzien = datetime.now()
        dzien_str = dzien.strftime("%Y-%m-%d")
        data = {"DataPoczatkowa": dzien_str, "DataKoncowa": dzien_str}
        j = self._post(self._full_url + "Uczen/Sprawdziany", json=data)
        sprawdziany = sorted(j["Data"], key=itemgetter("Data"))
        sprawdziany = list(filter(lambda x: x["DataTekst"] == dzien_str, sprawdziany))
        for sprawdzian in sprawdziany:
            sprawdzian["Przedmiot"] = find(
                self._dict["Przedmioty"], "Id", sprawdzian["IdPrzedmiot"]
            )
            sprawdzian["Pracownik"] = find(
                self._dict["Pracownicy"], "Id", sprawdzian["IdPracownik"]
            )
            sprawdzian["DataObjekt"] = datetime.fromtimestamp(sprawdzian["Data"]).date()
        return list(map(lambda x: Sprawdzian.from_json(x), sprawdziany))

    def zadania_domowe(self, dzien=None):
        """
        Pobiera zadania domowe z danego dnia

        Args:
            dzien (:class:`datetime.date` or :class:`datetime.datetime`): Dzień z którego pobrać
                zadania domowe, jeśli puste pobiera z aktualnego dnia

        Returns:
            :class:`list`: Listę zadań domowych
        """
        if not dzien:
            dzien = datetime.now()
        dzien_str = dzien.strftime("%Y-%m-%d")
        data = {"DataPoczatkowa": dzien_str, "DataKoncowa": dzien_str}
        j = self._post(self._full_url + "Uczen/ZadaniaDomowe", json=data)
        zadania_domowe = sorted(j["Data"], key=itemgetter("Data"))
        zadania_domowe = list(
            filter(lambda x: x["DataTekst"] == dzien_str, zadania_domowe)
        )
        for zadanie_domowe in zadania_domowe:
            zadanie_domowe["DataObjekt"] = datetime.fromtimestamp(
                zadanie_domowe["Data"]
            ).date()
            zadanie_domowe["Pracownik"] = find(
                self._dict["Pracownicy"], "Id", zadanie_domowe["IdPracownik"]
            )
            zadanie_domowe["Przedmiot"] = find(
                self._dict["Przedmioty"], "Id", zadanie_domowe["IdPrzedmiot"]
            )
        return list(map(lambda x: ZadanieDomowe.from_json(x), zadania_domowe))
