# -*- coding: utf-8 -*-

import pytest

from .utils import PARAMS_LESSON_PLAN


@pytest.mark.private
@pytest.mark.parametrize("date, lessons_expected", PARAMS_LESSON_PLAN)
class TestLessons:
    @pytest.mark.online
    @pytest.mark.asyncio
    async def test(self, client, date, lessons_expected):
        lessons = await client.get_lessons(date)

        async for lesson in lessons:
            assert lesson.date == date

    @pytest.mark.asyncio
    async def test_private(self, client, date, lessons_expected):
        lessons = await client.get_lessons(date)

        for i, lesson in enumerate([_ async for _ in lessons]):
            lesson_expected = lessons_expected[i]
            assert lesson.subject.id == lesson_expected["IdPrzedmiot"]
            assert lesson.teacher.id == lesson_expected["IdPracownik"]
