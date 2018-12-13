# -*- coding: utf-8 -*-

from os import environ
from datetime import date

PARAMS_LESSON_PLAN = [
    (date(2018, 9, 4), [
        {
            'IdPrzedmiot': 173,
            'IdPracownik': 99,
        },
        {
            'IdPrzedmiot': 123,
            'IdPracownik': 101,
        },
        {
            'IdPrzedmiot': 172,
            'IdPracownik': 92,
        },
        {
            'IdPrzedmiot': 189,
            'IdPracownik': 91,
        },
        {
            'IdPrzedmiot': 119,
            'IdPracownik': 100,
        },
        {
            'IdPrzedmiot': 175,
            'IdPracownik': 97,
        },
        {
            'IdPrzedmiot': 118,
            'IdPracownik': 89,
        },
    ])
]

PARAMS_TESTS = [
    (date(2018, 10, 5), [
        {
            'Id': 661,
            'IdPrzedmiot': 177,
            'IdPracownik': 87,
        },
    ]),
    (date(2018, 10, 23), [
        {
            'Id': 798,
            'IdPrzedmiot': 173,
            'IdPracownik': 99,
        },
        {
            'Id': 838,
            'IdPrzedmiot': 172,
            'IdPracownik': 92,
        },
    ]),
]

def load_variable(name):
    return environ.get(name)
