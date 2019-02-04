# -*- coding: utf-8 -*-

import pytest
from utils import *


@pytest.mark.private
@pytest.mark.parametrize("dzien, _lekcje", PARAMS_LESSON_PLAN)
class TestPlanLekcji(object):
    @pytest.mark.online
    def test(self, klient, dzien, _lekcje):
        lekcje = klient.plan_lekcji(dzien)
        for i, lekcja in enumerate(lekcje):
            assert lekcja["NumerLekcji"] == i + 1
            assert lekcja["DzienObjekt"] == dzien
            assert lekcja["IdPrzedmiot"] == lekcja["Przedmiot"]["Id"]
            assert lekcja["PrzedmiotNazwa"] == lekcja["Przedmiot"]["Nazwa"]
            assert lekcja["IdPracownik"] == lekcja["Pracownik"]["Id"]
            assert lekcja["IdPoraLekcji"] == lekcja["PoraLekcji"]["Id"]

    def test_private(self, klient, dzien, _lekcje):
        lekcje = klient.plan_lekcji(dzien)
        assert len(lekcje) == len(_lekcje)
        for i, lekcja in enumerate(lekcje):
            _lekcja = _lekcje[i]
            for k in _lekcja:
                assert lekcja[k] == _lekcja[k]
