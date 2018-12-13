# -*- coding: utf-8 -*-

import pytest
from utils import *

@pytest.mark.private
@pytest.mark.parametrize('date, _lessons', PARAMS_LESSON_PLAN)
class TestLessonPlan(object):

    @pytest.mark.online
    def test(self, client, date, _lessons):
        lessons = client.lesson_plan(date)
        for i, lesson in enumerate(lessons):
            assert lesson['NumerLekcji'] == i + 1
            assert lesson['DzienObjekt'] == date
            assert lesson['IdPrzedmiot'] == lesson['Przedmiot']['Id']
            assert lesson['PrzedmiotNazwa'] == lesson['Przedmiot']['Nazwa']
            assert lesson['IdPracownik'] == lesson['Pracownik']['Id']
            assert lesson['IdPoraLekcji'] == lesson['PoraLekcji']['Id']

    def test_private(self, client, date, _lessons):
        lessons = client.lesson_plan(date)
        assert len(lessons) == len(_lessons)
        for i, lesson in enumerate(lessons):
            _lesson = _lessons[i]
            for k in _lesson:
                assert lesson[k] == _lesson[k]


@pytest.mark.private
@pytest.mark.parametrize('date, _tests', PARAMS_TESTS)
class TestTests(object):

    @pytest.mark.online
    def test(self, client, date, _tests):
        tests = client.tests(date)
        for test in tests:
            assert test['DataObjekt'] == date
            assert test['IdPrzedmiot'] == test['Przedmiot']['Id']
            assert test['IdPracownik'] == test['Pracownik']['Id']

    def test_private(self, client, date, _tests):
        tests = client.tests(date)
        assert len(tests) == len(_tests)
        for i, test in enumerate(tests):
            _test = _tests[i]
            for k in _test:
                assert test[k] == _test[k]


@pytest.mark.private
@pytest.mark.parametrize('date, _homeworks', PARAMS_HOMEWORKS)
class TestHomeworks(object):

    def test(self, client, date, _homeworks):
        homeworks = client.homeworks(date)
        for homework in homeworks:
            assert homework['DataObjekt'] == date
            assert homework['IdPracownik'] == homework['Pracownik']['Id']
            assert homework['IdPrzedmiot'] == homework['Przedmiot']['Id']

    @pytest.mark.private
    def test_private(self, client, date, _homeworks):
        homeworks = client.homeworks(date)
        assert len(homeworks) == len(_homeworks)
        for i, homework in enumerate(homeworks):
            _homework = _homeworks[i]
            for k in _homework:
                assert homework[k] == _homework[k]
