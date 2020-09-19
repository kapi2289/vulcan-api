# -*- coding: utf-8 -*-

import pytest

from .utils import PARAMS_GRADES


@pytest.mark.online
@pytest.mark.parametrize("grades_expected", PARAMS_GRADES)
class TestGrades:
    def test(self, client, grades_expected):
        grades = client.get_grades()

        for grade_expected in grades_expected:
            grade = next(filter(lambda g: g.id == grade_expected["Id"], grades))

            assert grade.id == grade_expected["Id"]
            assert grade.teacher.id == grade_expected["IdPracownik"]
            assert grade.subject.id == grade_expected["IdPrzedmiot"]
            assert grade.content == grade_expected["Wpis"]
            assert grade.value == grade_expected["Wartosc"]
            assert grade.date == grade_expected["DataUtworzenia"]
