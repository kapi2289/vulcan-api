# -*- coding: utf-8 -*-

import pytest
from utils import *


@pytest.mark.private
@pytest.mark.parametrize('dzien, _zadania_domowe', PARAMS_HOMEWORKS)
class TestZadaniaDomowe(object):
    @pytest.mark.online
    def test(self, klient, dzien, _zadania_domowe):
        zadania_domowe = klient.zadania_domowe(dzien)
        for zadanie_domowe in zadania_domowe:
            assert zadanie_domowe['DataObjekt'] == dzien
            assert zadanie_domowe['IdPracownik'] == zadanie_domowe['Pracownik']['Id']
            assert zadanie_domowe['IdPrzedmiot'] == zadanie_domowe['Przedmiot']['Id']

    def test_private(self, klient, dzien, _zadania_domowe):
        zadania_domowe = klient.zadania_domowe(dzien)
        assert len(zadania_domowe) == len(_zadania_domowe)
        for i, zadanie_domowe in enumerate(zadania_domowe):
            _zadanie_domowe = _zadania_domowe[i]
            for k in _zadanie_domowe:
                assert zadanie_domowe[k] == _zadanie_domowe[k]
