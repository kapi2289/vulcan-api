# -*- coding: utf-8 -*-

import pytest
from utils import *

@pytest.mark.private
@pytest.mark.parametrize('date, lessons', PARAMS_LESSON_PLAN)
def test_lesson_plan_private(client, date, lessons):
    plan = client.lesson_plan(date)
    assert len(plan) == len(lessons)
    for i, lesson in enumerate(plan):
        assert lesson['NumerLekcji'] == i + 1
        assert lesson['DzienObjekt'] == date
        assert lesson['IdPrzedmiot'] == lesson['Przedmiot']['Id']
        assert lesson['PrzedmiotNazwa'] == lesson['Przedmiot']['Nazwa']
        assert lesson['IdPracownik'] == lesson['Pracownik']['Id']
        assert lesson['IdPoraLekcji'] == lesson['PoraLekcji']['Id']
        assert lesson['IdPrzedmiot'] == lessons[i]['IdPrzedmiot']
        assert lesson['IdPracownik'] == lessons[i]['IdPracownik']

@pytest.mark.online
@pytest.mark.parametrize('date, lessons', PARAMS_LESSON_PLAN)
def test_lesson_plan(client, date, lessons):
        client.lesson_plan(date)
