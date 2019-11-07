import pytest

from .utils import PARAMS_EXAMS


@pytest.mark.private
@pytest.mark.parametrize("date, exams_expected", PARAMS_EXAMS)
class TestExams:
    @pytest.mark.online
    def test(self, client, date, exams_expected):
        exams = client.get_exams(date)

        for exam in exams:
            assert exam.date == date

    def test_private(self, client, date, exams_expected):
        exams = client.get_exams(date)

        for i, exam in enumerate(exams):
            exam_expected = exams_expected[i]
            assert exam.id == exam_expected["Id"]
            assert exam.subject.id == exam_expected["IdPrzedmiot"]
            assert exam.teacher.id == exam_expected["IdPracownik"]
