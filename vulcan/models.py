# -*- coding: utf-8 -*-

from .utils import *
import json
import aenum


class VulcanAPIException(Exception):
    pass


class Plec(aenum.Enum):
    """Płeć"""
    KOBIETA = 0
    MEZCZYZNA = 1


class Okres(object):
    """
    Okres kwalifikacyjny

    Attributes:
        id (:class:`int`): ID okresu kwalifikacyjnego
        poziom (:class:`int`): Poziom (klasa) okresu kwalifikacyjnego
        numer (:class:`int`): Liczba kolejna okresu kwalifikacyjnego
        od (:class:`datetime.date`): Data rozpoczęcia okresu kwalifikacyjnego
        do (:class:`datetime.date`): Data zakończenia okresu kwalifikacyjnego
    """

    def __init__(self, id=None, poziom=None, numer=None, od=None, do=None):
        self.id = id
        self.poziom = poziom
        self.numer = numer
        self.od = od
        self.do = do

    def __repr__(self):
        return "<Okres: od={!r} do={!r}>".format(str(self.od), str(self.do))

    @classmethod
    def from_json(cls, j):
        id = j.get('IdOkresKlasyfikacyjny')
        poziom = j.get('OkresPoziom')
        numer = j.get('OkresNumer')
        od = timestamp_to_date(j['OkresDataOd']) if j.get('OkresDataOd') else None
        do = timestamp_to_date(j['OkresDataDo']) if j.get('OkresDataDo') else None
        return cls(
            id=id,
            poziom=poziom,
            numer=numer,
            od=od,
            do=do,
        )


class Klasa(object):
    """
    Oddział (klasa)

    Attributes:
        id (:class:`int`): ID klasy
        kod (:class:`str`): Kod klasy (np. `"8A"`)
        poziom (:class:`int`): Poziom klasy (np. `8`)
        symbol (:class:`str`): Symbol klasy (np. `"A"`)
    """

    def __init__(self, id=None, kod=None, poziom=None, symbol=None):
        self.id = id
        self.kod = kod
        self.poziom = poziom
        self.symbol = symbol

    def __repr__(self):
        return "<Klasa {!s}>".format(self.kod)

    @classmethod
    def from_json(cls, j):
        id = j.get('IdOddzial')
        kod = j.get('OddzialKod')
        poziom = j.get('OkresPoziom')
        symbol = j.get('OddzialSymbol')
        return cls(
            id=id,
            kod=kod,
            poziom=poziom,
            symbol=symbol,
        )


class Szkola(object):
    """
    Szkoła

    Attributes:
        id (:class:`int`) ID szkoły
        skrot (:class:`str`) Skrót nazwy szkoły
        nazwa (:class:`str`) Pełna nazwa szkoły
        symbol (:class:`str`) Symbol szkoły
    """

    def __init__(self, id=None, skrot=None, nazwa=None, symbol=None):
        self.id = id
        self.skrot = skrot
        self.nazwa = nazwa
        self.symbol = symbol

    def __repr__(self):
        return "<Szkola {!r}>".format(self.skrot)

    @classmethod
    def from_json(cls, j):
        id = j.get('IdJednostkaSprawozdawcza')
        skrot = j.get('JednostkaSprawozdawczaSkrot')
        nazwa = j.get('JednostkaSprawozdawczaNazwa')
        symbol = j.get('JednostkaSprawozdawczaSymbol')
        return cls(
            id=id,
            skrot=skrot,
            nazwa=nazwa,
            symbol=symbol,
        )


class Uczen(object):
    """
    Uczeń

    Attributes:
        id (:class:`int`): ID ucznia
        nazwa (:class:`str`): Nazwisko, imię oraz drugie imię ucznia
        imie (:class:`str`): Pierwsze imię ucznia
        drugie_imie (:class:`str` or :class:`None`): Drugie imię ucznia
        nazwisko (:class:`str`): Nazwisko ucznia
        pseudonim (:class:`str` or :class:`None`): Pseudonim ucznia
        plec (:class:`vulcan.models.Plec`): Płeć ucznia
        okres (:class:`vulcan.models.Okres`): Aktualny okres klasyfikacyjny ucznia
        klasa (:class:`vulcan.models.Klasa`): Klasa ucznia
        szkola (:class:`vulcan.models.Szkola`): Szkoła ucznia
    """

    def __init__(self, id=None, nazwa=None, imie=None, drugie_imie=None, nazwisko=None,
                    pseudonim=None, plec=None, okres=None, klasa=None, szkola=None):
        self.id = id
        self.nazwa = nazwa
        self.imie = imie
        self.drugie_imie = drugie_imie
        self.nazwisko = nazwisko
        self.pseudonim = pseudonim
        self.plec = plec
        self.okres = okres
        self.klasa = klasa
        self.szkola = szkola

    def __repr__(self):
        return "<Uczen {!r}>".format(self.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get('Id')
        nazwa = j.get('UzytkownikNazwa')
        imie = j.get('Imie')
        drugie_imie = j.get('Imie2') or None
        nazwisko = j.get('Nazwisko')
        pseudonim = j.get('Pseudonim')
        plec = Plec(j.get('UczenPlec'))
        okres = Okres.from_json(j)
        klasa = Klasa.from_json(j)
        szkola = Szkola.from_json(j)
        return cls(
            id=id,
            nazwa=nazwa,
            imie=imie,
            drugie_imie=drugie_imie,
            nazwisko=nazwisko,
            pseudonim=pseudonim,
            plec=plec,
            okres=okres,
            klasa=klasa,
            szkola=szkola,
        )


class Przedmiot(object):
    """
    Przedmiot

    Attributes:
        id (:class:`int`): ID przedmiotu
        nazwa (:class:`str`): Pełna nazwa przedmiotu
        kod (:class:`str`): Kod nazwy przedmiotu
    """

    def __init__(self, id=None, nazwa=None, kod=None):
        self.id = id
        self.nazwa = nazwa
        self.kod = kod

    def __repr__(self):
        return "<Przedmiot {!r}>".format(self.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get('Id')
        nazwa = j.get('Nazwa')
        kod = j.get('Kod')
        return cls(
            id=id,
            nazwa=nazwa,
            kod=kod,
        )


class Pracownik(object):
    """
    Pracownik szkoły

    Attributes:
        id (:class:`int`): ID pracownika
        nazwa (:class:`nazwa`): Nazwisko oraz imię pracownika
        imie (:class:`str`): Imię pracownika
        nazwisko (:class:`str`): Nazwisko pracownika
        kod (:class:`str`): Kod pracownika
        login_id (:class:`int`): ID konta pracownika
    """

    def __init__(self, id=None, imie=None, nazwisko=None, kod=None, login_id=None):
        self.id = id
        self.nazwa = "{!s} {!s}".format(nazwisko, imie)
        self.imie = imie
        self.nazwisko = nazwisko
        self.kod = kod
        self.login_id = login_id

    def __repr__(self):
        return "<Pracownik {!r}>".format(self.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get('Id')
        imie = j.get('Imie')
        nazwisko = j.get('Nazwisko')
        kod = j.get('Kod')
        login_id = j.get('LoginId')
        return cls(
            id=id,
            imie=imie,
            nazwisko=nazwisko,
            kod=kod,
            login_id=login_id,
        )


class Lekcja(object):
    """
    Lekcja

    Attributes:
        numer (:class:`int`): Numer lekcji
        pora (): Informacje o porze lekcji
        przedmiot (:class:`vulcan.models.Przedmiot`): Przedmiot na lekcji
        dzien (:class:`datetime.date`): Data lekcji
    """

    def __init__(self, numer=None, pora=None, przedmiot=None, pracownik=None,
                dzien=None, od=None, do=None):
        self.numer = numer
        self.pora =  pora
        self.przedmiot = przedmiot
        self.pracownik = pracownik
        self.dzien = dzien

    def __repr__(self):
        return "<Lekcja {!s}>".format(self.numer)

    @classmethod
    def from_json(cls, j):
        numer = j.get('NumerLekcji')
        przedmiot = Przedmiot.from_json(j.get('Przedmiot'))
        pracownik = Pracownik.from_json(j.get('Pracownik'))
        dzien = timestamp_to_date(j.get('Dzien'))
        return cls(
            numer=numer,
            przedmiot=przedmiot,
            pracownik=pracownik,
            dzien=dzien,
        )
