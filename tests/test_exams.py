# -*- coding: utf-8 -*-

from datetime import date

import pytest

from .utils import PARAMS_EXAMS


@pytest.mark.online
@pytest.mark.parametrize("exams_expected", PARAMS_EXAMS)
class TestExams:
    def test(self, client, exams_expected):
        exams = client.get_exams()

        for i, exam in enumerate(exams):
            exam_expected = exams_expected[i]
            assert exam.id == exam_expected["Id"]
            assert exam.subject.id == exam_expected["IdPrzedmiot"]
            assert exam.teacher.id == exam_expected["IdPracownik"]
            assert exam.description == exam_expected["Opis"]
            assert exam.date == date.today()
