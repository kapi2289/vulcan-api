# -*- coding: utf-8 -*-

from datetime import date, datetime
from os import environ

PARAMS_LESSON_PLAN = [
    (
        date(2019, 9, 20),
        [
            {"IdPrzedmiot": 189, "IdPracownik": 91},
            {"IdPrzedmiot": 177, "IdPracownik": 131},
            {"IdPrzedmiot": 172, "IdPracownik": 99},
            {"IdPrzedmiot": 362, "IdPracownik": 94},
            {"IdPrzedmiot": 118, "IdPracownik": 94},
            {"IdPrzedmiot": 119, "IdPracownik": 101},
        ],
    )
]

PARAMS_EXAMS = [
    (date(2019, 9, 25), [{"Id": 2118, "IdPrzedmiot": 118, "IdPracownik": 94}]),
    (
        date(2019, 10, 24),
        [
            {"Id": 2308, "IdPrzedmiot": 118, "IdPracownik": 94},
            {"Id": 2317, "IdPrzedmiot": 164, "IdPracownik": 89},
        ],
    ),
]

PARAMS_HOMEWORK_LIST = [
    (
        date(2019, 9, 24),
        [
            {"Id": 886, "IdPracownik": 94, "IdPrzedmiot": 118},
            {"Id": 875, "IdPracownik": 100, "IdPrzedmiot": 119},
        ],
    )
]

PARAMS_GRADES = [
    (
        [
            {
                "Id": 227084,
                "IdPracownik": 99,
                "IdPrzedmiot": 172,
                "Wpis": "4",
                "Wartosc": 4.0,
                "DataUtworzenia": datetime(2020, 1, 29),
            },
            {
                "Id": 230461,
                "IdPracownik": 85,
                "IdPrzedmiot": 183,
                "Wpis": "-",
                "Wartosc": None,
                "DataUtworzenia": datetime(2020, 2, 25),
            },
        ]
    )
]

PARAMS_MESSAGES = [
    (
        [
            {
                "WiadomoscId": 11544,
                "NadawcaId": 494,
                "Tytul": "Sprawdzian z części zdań ",
                "Tresc": "Dzień dobry państwu",
                "DataWyslania": "06.02.2020",
                "DataPrzeczytania": "06.02.2020",
            },
            {
                "WiadomoscId": 12027,
                "NadawcaId": 484,
                "Tytul": "Zasady postępowania przy zagrożeniu koronawirusem",
                "Tresc": "REKOMENDACJE MINISTRA EDUKACJI NARODOWEJ",
                "DataWyslania": "10.03.2020",
                "DataPrzeczytania": "10.03.2020",
            },
        ]
    )
]

PARAMS_DICTIONARIES_TEACHERS = [(85, 477, "ET"), (91, 482, "GD"), (95, 491, "MK")]

PARAMS_DICTIONARIES_SUBJECTS = [
    (115, "Religia", "religia", 0),
    (118, "Język polski", "j. polski", 2),
    (170, "Wiedza o społeczeństwie", "wos", 7),
]

PARAMS_DICTIONARIES_LESSON_TIMES = [
    (36, 1, "08:15", "09:00"),
    (37, 2, "09:10", "09:55"),
    (42, 7, "13:55", "14:40"),
]

PARAMS_DICTIONARIES_GRADE_CATEGORIES = [
    (15, "Akt", "Aktywność na lekcji"),
    (31, "Proj", "Projekt długoterminowy do domu"),
    (32, "PL", "Praca na lekcji"),
]


def load_variable(name):
    return environ.get(name)
