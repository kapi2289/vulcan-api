# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ._api import Api
from ._certificate import Certificate
from ._exam import Exam
from ._grade import Grade
from ._homework import Homework
from ._lesson import Lesson
from ._message import Message
from ._student import Student
from ._utils import log


class Vulcan:
    """
    Logs in to the e-register using generated certificate

    Args:
        certificate (:class:`dict`): Generated certificate
            using :func:`vulcan.Vulcan.register`
    """

    def __init__(self, certificate, logging_level=None):
        self._api = Api(certificate)

        if logging_level:
            Vulcan.set_logging_level(logging_level)

    async def setup(self):
        self.students = await self.get_students()
        await self.set_student(await self.students.__anext__())

    @staticmethod
    async def create(certificate, logging_level=None):
        api = Vulcan(certificate, logging_level)
        await api.setup()
        return api

    @staticmethod
    def set_logging_level(logging_level):
        """
        Sets the default logging level

        Args:
            logging_level (:class:`int`): Logging level from :module:`logging` module
        """

        log.setLevel(logging_level)

    @staticmethod
    async def register(token, symbol, pin):
        """
        Registers API as a new mobile device

        Args:
            token (:class:`str`): Token
            symbol (:class:`str`): Symbol
            pin (:class:`str`): PIN code

        Returns:
            :class:`vulcan._certificate.Certificate`: Generated certificate, use `json` property to save it to a file
        """
        return await Certificate.get(token, symbol, pin)

    async def get_students(self):
        """
        Yields students that are assigned to the account

        Yields:
            :class:`vulcan._student.Student`
        """
        return Student.get(self._api)

    async def set_student(self, student):
        """
        Sets the default student

        Args:
            student (:class:`vulcan._student.Student`): Student from :func:`vulcan.Vulcan.get_students`
        """
        await self._api.set_student(student)

    @property
    def dictionaries(self):
        """
        :class:`vulcan._dictionaries.Dictionaries`: Dictionaries, that include i.a. teachers
        """
        return self._api.dict

    async def get_grades(self):
        """
        Fetches student grades

        Yields:
            :class:`vulcan._grade.Grade`
        """
        return Grade.get(self._api)

    async def get_lessons(self, date=None):
        """
        Fetches lessons from the given date

        Args:
            date (:class:`datetime.date`): Date, from which to fetch lessons, if not provided
                it's using the today date

        Yields:
            :class:`vulcan._lesson.Lesson`
        """
        return Lesson.get(self._api, date)

    async def get_exams(self, date=None):
        """
        Fetches exams from the given date

        Args:
            date (:class:`datetime.date`): Date, from which to fetch exams, if not provided
                it's using the today date

        Yields:
            :class:`vulcan._exam.Exam`
        """
        return Exam.get(self._api, date)

    async def get_homework(self, date=None):
        """
        Fetches homework from the given date

        Args:
            date (:class:`datetime.date`): Date, from which to fetch exams, if not provided
                it's using the today date

        Yields:
            :class:`vulcan._homework.Homework`
        """
        return Homework.get(self._api, date)

    async def get_messages(self, date_from=None, date_to=None):
        """
        Fetches messages from the given date

        Args:
            date_from (:class:`datetime.date`): Date, from which to fetch messages, if not provided
                it's using the semester (period) start date
            date_to (:class:`datetime.date`): Date, to which to fetch messages, if not provided
                it's using the semester (period) end date

        Yields:
            :class:`vulcan._message.Message`
        """
        return Message.get(self._api, date_from, date_to)

    async def close(self):
        await self._api.close()

    def __del__(self):
        import asyncio
        asyncio.run(self.close())
