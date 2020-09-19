# -*- coding: utf-8 -*-

from datetime import date

import pytest

from .utils import PARAMS_HOMEWORK_LIST


@pytest.mark.online
@pytest.mark.parametrize("homework_expected_list", PARAMS_HOMEWORK_LIST)
class TestHomework:
    def test(self, client, homework_expected_list):
        homework_list = client.get_homework()

        for i, homework in enumerate(homework_list):
            homework_expected = homework_expected_list[i]
            assert homework.id == homework_expected["Id"]
            assert homework.subject.id == homework_expected["IdPrzedmiot"]
            assert homework.teacher.id == homework_expected["IdPracownik"]
            assert homework.description == homework_expected["Opis"]
            assert homework.date == date.today()
