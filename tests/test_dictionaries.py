# -*- coding: utf-8 -*-

import pytest

from .utils import (
    PARAMS_DICTIONARIES_TEACHERS,
    PARAMS_DICTIONARIES_SUBJECTS,
    PARAMS_DICTIONARIES_LESSON_TIMES,
    PARAMS_DICTIONARIES_GRADE_CATEGORIES,
)


@pytest.mark.private
class TestDictionaries:
    @pytest.mark.parametrize("_id, login_id, short", PARAMS_DICTIONARIES_TEACHERS)
    def test_teachers(self, client, _id, login_id, short):
        teacher = next(filter(lambda t: t.id == _id, client.dictionaries.teachers))
        assert teacher.short == short
        assert teacher.login_id == login_id

    @pytest.mark.parametrize("_id, name, short, position", PARAMS_DICTIONARIES_SUBJECTS)
    def test_subjects(self, client, _id, name, short, position):
        subject = next(filter(lambda s: s.id == _id, client.dictionaries.subjects))
        assert subject.name == name
        assert subject.short == short
        assert subject.position == position

    @pytest.mark.parametrize("_id, number, from_, to", PARAMS_DICTIONARIES_LESSON_TIMES)
    def test_lesson_times(self, client, _id, number, from_, to):
        lesson_time = next(
            filter(lambda t: t.id == _id, client.dictionaries.lesson_times)
        )
        assert lesson_time.number == number
        assert lesson_time.from_.strftime("%H:%M") == from_
        assert lesson_time.to.strftime("%H:%M") == to

    @pytest.mark.parametrize("_id, short, name", PARAMS_DICTIONARIES_GRADE_CATEGORIES)
    def test_grade_categories(self, client, _id, short, name):
        grade_category = next(
            filter(lambda c: c.id == _id, client.dictionaries.grade_categories)
        )
        assert grade_category.short == short
        assert grade_category.name == name
