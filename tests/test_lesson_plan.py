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
