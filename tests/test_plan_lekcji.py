import pytest

from .utils import *


@pytest.mark.private
@pytest.mark.parametrize("dzien, _lekcje", PARAMS_LESSON_PLAN)
class TestPlanLekcji:
    @pytest.mark.online
    def test(self, klient, dzien, _lekcje):
        lekcje = klient.plan_lekcji(dzien)
        for i, lekcja in enumerate(lekcje):
            assert lekcja.dzien == dzien

    def test_private(self, klient, dzien, _lekcje):
        lekcje = klient.plan_lekcji(dzien)
        assert len(lekcje) == len(_lekcje)
        for i, lekcja in enumerate(lekcje):
            _lekcja = _lekcje[i]
            assert lekcja.przedmiot.id == _lekcja["IdPrzedmiot"]
            assert lekcja.pracownik.id == _lekcja["IdPracownik"]
