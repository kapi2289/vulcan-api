# -*- coding: utf-8 -*-

import pytest

from .utils import PARAMS_HOMEWORK_LIST


@pytest.mark.private
@pytest.mark.parametrize("date, homework_expected_list", PARAMS_HOMEWORK_LIST)
class TestHomework:
    @pytest.mark.online
    @pytest.mark.asyncio
    async def test(self, client, date, homework_expected_list):
        homework_list = await client.get_homework(date)

        async for homework in homework_list:
            assert homework.date == date

    @pytest.mark.asyncio
    async def test_private(self, client, date, homework_expected_list):
        homework_list = await client.get_homework(date)

        for i, homework in enumerate([_ async for _ in homework_list]):
            homework_expected = homework_expected_list[i]
            assert homework.id == homework_expected["Id"]
            assert homework.subject.id == homework_expected["IdPrzedmiot"]
            assert homework.teacher.id == homework_expected["IdPracownik"]
