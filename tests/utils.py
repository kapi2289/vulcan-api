# -*- coding: utf-8 -*-

from datetime import date
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
            {"Id": 875, "IdPracownik": 100, "IdPrzedmiot": 119},
            {"Id": 886, "IdPracownik": 94, "IdPrzedmiot": 118},
        ],
    )
]


def load_variable(name):
    return environ.get(name)
