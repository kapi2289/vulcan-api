# -*- coding: utf-8 -*-

from .utils import *
import json
import aenum


class VulcanAPIException(Exception):
    pass


class Plec(aenum.Enum):
    KOBIETA = 0
    MEZCZYZNA = 1


class Okres(object):

    def __init__(self, id=None, poziom=None, numer=None, od=None, do=None):
        #: ID okresu kwalifikacyjnego
        self.id = id
        #: Poziom (klasa) okresu kwalifikacyjnego
        self.poziom = poziom
        #: Liczba kolejna okresu kwalifikacyjnego
        self.numer = numer
        #: Data rozpoczęcia okresu kwalifikacyjnego
        self.od = od
        #: Data zakończenia okresu kwalifikacyjnego
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

    def __init__(self, id=None, kod=None, poziom=None, symbol=None):
        #: ID klasy
        self.id = id
        #: Kod klasy (np. '8A')
        self.kod = kod
        #: Poziom klasy (np. 8)
        self.poziom = poziom
        #: Symbol klasy (np. 'A')
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

    def __init__(self, id=None, nazwa=None, imie=None, drugie_imie=None, nazwisko=None,
                    pseudonim=None, plec=None, okres=None, klasa=None, szkola=None):
        #: ID ucznia
        self.id = id
        #: Nazwisko, imię oraz drugie imię ucznia
        self.nazwa = nazwa
        #: Pierwsze imię ucznia
        self.imie = imie
        #: Drugie imię ucznia
        self.drugie_imie = drugie_imie
        #: Nazwisko ucznia
        self.nazwisko = nazwisko
        #: Pseudonim ucznia
        self.pseudonim = pseudonim
        #: Płeć ucznia
        self.plec = plec
        #: Aktualny okres klasyfikacyjny ucznia
        self.okres = okres
        #: Klasa ucznia
        self.klasa = klasa
        #: Szkoła ucznia
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
