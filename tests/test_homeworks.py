# -*- coding: utf-8 -*-

import pytest
from utils import *


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
