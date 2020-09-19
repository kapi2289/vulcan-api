# -*- coding: utf-8 -*-

from datetime import date

import pytest

from .utils import PARAMS_LESSON_PLAN


@pytest.mark.online
@pytest.mark.parametrize("lessons_expected", PARAMS_LESSON_PLAN)
class TestLessons:
    @pytest.mark.online
    def test(self, client, lessons_expected):
        lessons = client.get_lessons()

        for i, lesson in enumerate(lessons):
            try:
                lesson_expected = lessons_expected[i]
            except IndexError:
                break

            if lesson.subject:
                assert lesson.subject.id == lesson_expected["IdPrzedmiot"]
            assert lesson.teacher.id == lesson_expected["IdPracownik"]
            assert lesson.date == date.today()
