# -*- coding: utf-8 -*-

import pytest
from utils import *


@pytest.mark.private
@pytest.mark.parametrize("dzien, _zadania_domowe", PARAMS_HOMEWORKS)
class TestZadaniaDomowe(object):
    @pytest.mark.online
    def test(self, klient, dzien, _zadania_domowe):
        zadania_domowe = klient.zadania_domowe(dzien)
        for zadanie_domowe in zadania_domowe:
            assert zadanie_domowe.dzien == dzien

    def test_private(self, klient, dzien, _zadania_domowe):
        zadania_domowe = klient.zadania_domowe(dzien)
        assert len(zadania_domowe) == len(_zadania_domowe)
        for i, zadanie_domowe in enumerate(zadania_domowe):
            _zadanie_domowe = _zadania_domowe[i]
            assert zadanie_domowe.id == _zadanie_domowe["Id"]
            assert zadanie_domowe.przedmiot.id == _zadanie_domowe["IdPrzedmiot"]
            assert zadanie_domowe.pracownik.id == _zadanie_domowe["IdPracownik"]
