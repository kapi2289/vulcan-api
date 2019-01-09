# -*- coding: utf-8 -*-

import json
import aenum


class VulcanAPIException(Exception):
    pass


class Plec(aenum.Enum):
    KOBIETA = 0
    MEZCZYZNA = 1


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
        drugie_imie = j['Imie2'] if j.get('Imie2') else None
        nazwisko = j.get('Nazwisko')
        pseudonim = j.get('Pseudonim')
        plec = Plec(j.get('UczenPlec'))
        return cls(
            id=id,
            nazwa=nazwa,
            imie=imie,
            drugie_imie=drugie_imie,
            nazwisko=nazwisko,
            pseudonim=pseudonim,
            plec=plec,
        )
