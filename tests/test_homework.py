import pytest

from .utils import PARAMS_HOMEWORK_LIST


@pytest.mark.private
@pytest.mark.parametrize("date, homework_expected_list", PARAMS_HOMEWORK_LIST)
class TestHomework:
    @pytest.mark.online
    def test(self, client, date, homework_expected_list):
        homework_list = client.get_homework(date)

        for homework in homework_list:
            assert homework.date == date

    def test_private(self, client, date, homework_expected_list):
        homework_list = client.get_homework(date)
        assert len(homework_list) == len(homework_expected_list)

        for i, homework in enumerate(homework_list):
            homework_expected = homework_expected_list[i]
            assert homework.id == homework_expected["Id"]
            assert homework.subject.id == homework_expected["IdPrzedmiot"]
            assert homework.teacher.id == homework_expected["IdPracownik"]
