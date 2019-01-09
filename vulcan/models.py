# -*- coding: utf-8 -*-

import json


class VulcanAPIException(Exception):
    pass


class Uczen(object):
    #: ID ucznia
    id: int = None
    #: Nazwisko, imię oraz drugie imię ucznia
    nazwa: str = None
    #: Pierwsze imię ucznia
    imie: str = None
    #: Drugie imię ucznia
    drugie_imie: str = None
    #: Nazwisko ucznia
    nazwisko: str = None
    #: Pseudonim ucznia
    pseudonim: str = None
    #: Płeć ucznia
    plec = None
    #: Aktualny okres klasyfikacyjny ucznia
    okres = None
    #: Klasa ucznia
    klasa = None
    #: Szkoła ucznia
    szkola = None

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
    def from_json(cls, j: dict):
        id = j.get('Id')
        nazwa = j.get('UzytkownikNazwa')
        imie = j.get('Imie')
        drugie_imie = j['Imie2'] if j.get('Imie2') else None
        nazwisko = j.get('Nazwisko')
        pseudonim = j.get('Pseudonim')
        return cls(
            id=id,
            nazwa=nazwa,
            imie=imie,
            drugie_imie=drugie_imie,
            nazwisko=nazwisko,
            pseudonim=pseudonim,
        )
