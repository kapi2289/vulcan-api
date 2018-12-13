# -*- coding: utf-8 -*-

import pytest
from utils import *


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
