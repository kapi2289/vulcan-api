import pytest

from .utils import *


@pytest.mark.private
@pytest.mark.parametrize("dzien, _sprawdziany", PARAMS_TESTS)
class TestSprawdziany:
    @pytest.mark.online
    def test(self, klient, dzien, _sprawdziany):
        sprawdziany = klient.sprawdziany(dzien)
        for sprawdzian in sprawdziany:
            assert sprawdzian.date == dzien

    def test_private(self, klient, dzien, _sprawdziany):
        sprawdziany = klient.sprawdziany(dzien)
        assert len(sprawdziany) == len(_sprawdziany)
        for i, sprawdzian in enumerate(sprawdziany):
            _sprawdzian = _sprawdziany[i]
            assert sprawdzian.id == _sprawdzian["Id"]
            assert sprawdzian.subject.id == _sprawdzian["IdPrzedmiot"]
            assert sprawdzian.teacher.id == _sprawdzian["IdPracownik"]
