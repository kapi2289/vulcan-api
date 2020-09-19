# -*- coding: utf-8 -*-

from datetime import datetime
from os import environ

PARAMS_LESSON_PLAN = [
    [
        {"NumerLekcji": 1, "IdPrzedmiot": 308, "IdPracownik": 1},
        {"NumerLekcji": 2, "IdPrzedmiot": 499, "IdPracownik": 8},
        {"NumerLekcji": 2, "IdPrzedmiot": 499, "IdPracownik": 7},
        {"NumerLekcji": 4, "IdPrzedmiot": 300, "IdPracownik": 4},
    ]
]

PARAMS_EXAMS = [
    [
        {
            "Id": 21558,
            "IdPrzedmiot": 307,
            "IdPracownik": 3,
            "Opis": "Figury na płaszczyźnie.",
        },
        {
            "Id": 22067,
            "IdPrzedmiot": 304,
            "IdPracownik": 6,
            "Opis": "czasowniki nieregualne 1 częsć",
        },
        {
            "Id": 23031,
            "IdPrzedmiot": 311,
            "IdPracownik": 2,
            "Opis": "Opolszczyzna - mapa",
        },
    ]
]

PARAMS_HOMEWORK_LIST = [
    [
        {
            "Id": 1,
            "IdPracownik": 5,
            "IdPrzedmiot": 306,
            "Opis": "Wszystkie instrukcje warunkowe, pętle (budowa, zasada działania, schemat blokowy)",
        },
        {
            "Id": 2,
            "IdPracownik": 7,
            "IdPrzedmiot": 304,
            "Opis": "Zadania egzaminacyjne:\nstr 231 \nstr 254",
        },
    ]
]

PARAMS_GRADES = [
    [
        {
            "Id": 1000,
            "IdPracownik": 1,
            "IdPrzedmiot": 300,
            "Wpis": "3",
            "Wartosc": 3.0,
            "DataUtworzenia": datetime(2018, 9, 14),
        },
        {
            "Id": 1021,
            "IdPracownik": 10,
            "IdPrzedmiot": 313,
            "Wpis": "75/100",
            "Wartosc": 0.0,
            "DataUtworzenia": datetime(2018, 11, 20),
        },
    ]
]

PARAMS_MESSAGES = [
    (
        [
            {
                "WiadomoscId": 27214,
                "NadawcaId": 3617,
                "Tytul": "Temat wiadomości",
                "Tresc": "Tak wygląda zawartość wiadomości.\nZazwyczaj ma wiele linijek.",
                "DataWyslania": "01.03.2018",
                "DataPrzeczytania": None,
            },
            {
                "WiadomoscId": 28973,
                "NadawcaId": 2137,
                "Tytul": "Tytuł",
                "Tresc": "Bardzo dużo",
                "DataWyslania": "05.04.2018",
                "DataPrzeczytania": None,
            },
        ]
    )
]

PARAMS_DICTIONARIES_TEACHERS = [
    (1, 100, "AN", "Karolina Kowalska"),
    (2, 101, "NA", "Zofia Czerwińska"),
    (3, 102, "AK", "Aleksandra Krajewska"),
]

PARAMS_DICTIONARIES_SUBJECTS = [
    (300, "Zajęcia z wychowawcą", "godz.wych", 0),
    (301, "Język polski", "j. polski", 3),
    (302, "Historia", "historia", 1),
]

PARAMS_DICTIONARIES_LESSON_TIMES = [
    (76, 1, "08:00", "08:45"),
    (77, 2, "08:55", "09:40"),
    (82, 7, "13:40", "14:25"),
]

PARAMS_DICTIONARIES_GRADE_CATEGORIES = [
    (26, "Akt", "A - aktywność (czarny)"),
    (74, "pr_dł", "Praca długoterminowa"),
    (78, "PK", "Praca klasowa"),
]


def load_variable(name):
    return environ.get(name)
