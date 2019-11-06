# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import platform
from datetime import datetime
from operator import itemgetter

import requests

from ._utils import (
    log,
    uuid,
    now,
    get_base_url,
    VulcanAPIException,
    find,
    signature,
    sort_and_filter_date,
)
from .models import Uczen, Ocena, Lekcja, Sprawdzian, ZadanieDomowe


class Vulcan:
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
        self._url = certyfikat["AdresBazowyRestApi"]
        self._base_url = self._url + "mobile-api/Uczen.v3."
        self._full_url = None
        self._dict = None

        if logging_level:
            Vulcan.set_logging_level(logging_level)

        self.uczen = None
        uczniowie = self.uczniowie()
        self.ustaw_ucznia(uczniowie[0])

    @staticmethod
    def set_logging_level(logging_level):
        """
        Ustawia poziom logowania

        Args:
            logging_level (:class:`int`): Poziom logowania z modułu :module:`logging`
        """

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

        base_url = get_base_url(token)
        url = "{}/{}/mobile-api/Uczen.v3.UczenStart/Certyfikat".format(base_url, symbol)

        log.info("Rejestrowanie...")

        r = requests.post(url, json=data, headers=headers)
        j = r.json()
        log.debug(j)

        cert = j["TokenCert"]
        assert cert
        log.info("Zarejestrowano pomyślnie!")
        return cert

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
                raise VulcanAPIException("Wystąpił błąd.")

        return r

    def _get(self, endpoint, json=None, as_json=True, **kwargs):
        return self._request("GET", endpoint, json=json, as_json=as_json, **kwargs)

    def _post(self, endpoint, json=None, as_json=True, **kwargs):
        return self._request("POST", endpoint, json=json, as_json=as_json, **kwargs)

    def _get_dict(self):
        j = self._post("Uczen/Slowniki")
        return j["Data"]

    def _get_dict_value(self, _id, dict_key):
        return find(self._dict[dict_key], "Id", _id)

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

    def oceny(self):
        """
        Pobiera oceny cząstkowe

        Returns:
            :class:`list`: Listę ocen cząstkowych
        """

        j = self._post("Uczen/Oceny")

        if j.get("Data"):
            oceny = j["Data"]

            for ocena in oceny:
                ocena["Przedmiot"] = self._get_dict_value(
                    ocena["IdPrzedmiot"], "Przedmioty"
                )
                ocena["Kategoria"] = self._get_dict_value(
                    ocena["IdKategoria"], "KategorieOcen"
                )
                ocena["Pracownik"] = self._get_dict_value(
                    ocena["IdPracownikD"], "Pracownicy"
                )

            return list(map(lambda x: Ocena.from_json(x), oceny))
        else:
            return list()

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

        j = self._post("Uczen/PlanLekcjiZeZmianami", json=data)

        if j.get("Data"):
            plan_lekcji = sorted(j["Data"], key=itemgetter("NumerLekcji"))
            plan_lekcji = list(
                filter(lambda x: x["DzienTekst"] == dzien_str, plan_lekcji)
            )

            for lekcja in plan_lekcji:
                lekcja["PoraLekcji"] = self._get_dict_value(
                    lekcja["IdPoraLekcji"], "PoryLekcji"
                )
                lekcja["Przedmiot"] = self._get_dict_value(
                    lekcja["IdPrzedmiot"], "Przedmioty"
                )
                lekcja["Pracownik"] = self._get_dict_value(
                    lekcja["IdPracownik"], "Pracownicy"
                )
                lekcja["PracownikWspomagajacy"] = self._get_dict_value(
                    lekcja["IdPracownikWspomagajacy"], "Pracownicy"
                )

            return list(map(lambda x: Lekcja.from_json(x), plan_lekcji))
        else:
            return list()

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

        j = self._post("Uczen/Sprawdziany", json=data)

        if j.get("Data"):
            sprawdziany = sort_and_filter_date(j["Data"], dzien_str)

            for sprawdzian in sprawdziany:
                sprawdzian["Przedmiot"] = self._get_dict_value(
                    sprawdzian["IdPrzedmiot"], "Przedmioty"
                )
                sprawdzian["Pracownik"] = self._get_dict_value(
                    sprawdzian["IdPracownik"], "Pracownicy"
                )

            return list(map(lambda x: Sprawdzian.from_json(x), sprawdziany))
        else:
            return list()

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

        j = self._post("Uczen/ZadaniaDomowe", json=data)

        if j.get("Data"):
            zadania_domowe = sort_and_filter_date(j["Data"], dzien_str)

            for zadanie_domowe in zadania_domowe:
                zadanie_domowe["Pracownik"] = self._get_dict_value(
                    zadanie_domowe["IdPracownik"], "Pracownicy"
                )
                zadanie_domowe["Przedmiot"] = self._get_dict_value(
                    zadanie_domowe["IdPrzedmiot"], "Przedmioty"
                )

            return list(map(lambda x: ZadanieDomowe.from_json(x), zadania_domowe))
        else:
            return list()
