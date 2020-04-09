# -*- coding: utf-8 -*-

import pytest

from .utils import PARAMS_EXAMS


@pytest.mark.private
@pytest.mark.parametrize("date, exams_expected", PARAMS_EXAMS)
class TestExams:
    @pytest.mark.online
    @pytest.mark.asyncio
    async def test(self, client, date, exams_expected):
        exams = await client.get_exams(date)

        async for exam in exams:
            assert exam.date == date

    @pytest.mark.asyncio
    async def test_private(self, client, date, exams_expected):
        exams = await client.get_exams(date)

        for i, exam in enumerate([_ async for _ in exams]):
            exam_expected = exams_expected[i]
            assert exam.id == exam_expected["Id"]
            assert exam.subject.id == exam_expected["IdPrzedmiot"]
            assert exam.teacher.id == exam_expected["IdPracownik"]
