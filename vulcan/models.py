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
        szkola (): Szkoła ucznia
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
        )
