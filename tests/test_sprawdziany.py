# -*- coding: utf-8 -*-

import pytest
from utils import *


@pytest.mark.private
@pytest.mark.parametrize("dzien, _sprawdziany", PARAMS_TESTS)
class TestSprawdziany(object):
    @pytest.mark.online
    def test(self, klient, dzien, _sprawdziany):
        sprawdziany = klient.sprawdziany(dzien)
        for sprawdzian in sprawdziany:
            assert sprawdzian["DataObjekt"] == dzien
            assert sprawdzian["IdPrzedmiot"] == sprawdzian["Przedmiot"]["Id"]
            assert sprawdzian["IdPracownik"] == sprawdzian["Pracownik"]["Id"]

    def test_private(self, klient, dzien, _sprawdziany):
        sprawdziany = klient.sprawdziany(dzien)
        assert len(sprawdziany) == len(_sprawdziany)
        for i, sprawdzian in enumerate(sprawdziany):
            _sprawdzian = _sprawdziany[i]
            for k in _sprawdzian:
                assert sprawdzian[k] == _sprawdzian[k]
