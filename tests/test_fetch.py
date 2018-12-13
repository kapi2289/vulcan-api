# -*- coding: utf-8 -*-

import pytest
from utils import *

@pytest.mark.private
@pytest.mark.online
@pytest.mark.parametrize('date, _lessons', PARAMS_LESSON_PLAN)
def test_lesson_plan(client, date, _lessons):
    lessons = client.lesson_plan(date)
    for i, lesson in enumerate(lessons):
        assert lesson['NumerLekcji'] == i + 1
        assert lesson['DzienObjekt'] == date
        assert lesson['IdPrzedmiot'] == lesson['Przedmiot']['Id']
        assert lesson['PrzedmiotNazwa'] == lesson['Przedmiot']['Nazwa']
        assert lesson['IdPracownik'] == lesson['Pracownik']['Id']
        assert lesson['IdPoraLekcji'] == lesson['PoraLekcji']['Id']

@pytest.mark.private
@pytest.mark.parametrize('date, _lessons', PARAMS_LESSON_PLAN)
def test_lesson_plan_private(client, date, _lessons):
    lessons = client.lesson_plan(date)
    assert len(lessons) == len(_lessons)
    for i, lesson in enumerate(lessons):
        _lesson = _lessons[i]
        for k in _lesson:
            assert lesson[k] == _lesson[k]

@pytest.mark.private
@pytest.mark.online
@pytest.mark.parametrize('date, _tests', PARAMS_TESTS)
def test_tests(client, date, _tests):
    tests = client.tests(date)
    for test in tests:
        assert test['DataObjekt'] == date
        assert test['IdPrzedmiot'] == test['Przedmiot']['Id']
        assert test['IdPracownik'] == test['Pracownik']['Id']

@pytest.mark.private
@pytest.mark.parametrize('date, _tests', PARAMS_TESTS)
def test_tests_private(client, date, _tests):
    tests = client.tests(date)
    assert len(tests) == len(_tests)
    for i, test in enumerate(tests):
        _test = _tests[i]
        for k in _test:
            assert test[k] == _test[k]
