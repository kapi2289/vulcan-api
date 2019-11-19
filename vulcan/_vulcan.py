# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ._api import Api
from ._certificate import Certificate
from ._exam import Exam
from ._grade import Grade
from ._homework import Homework
from ._lesson import Lesson
from ._student import Student
from ._utils import log


class Vulcan:
    """
    Logs in to the e-register using generated certificate

    Args:
        certificate (:class:`dict`): Certyfikat wygenerowany za pomocą :func:`vulcan.Vulcan.register`
    """

    def __init__(self, certificate, logging_level=None):
        self._api = Api(certificate)

        if logging_level:
            Vulcan.set_logging_level(logging_level)

        self.students = self.get_students()
        self.set_student(next(self.students))

    @staticmethod
    def set_logging_level(logging_level):
        """
        Sets the default logging level

        Args:
            logging_level (:class:`int`): Logging level from :module:`logging` module
        """

        log.setLevel(logging_level)

    @staticmethod
    def register(token, symbol, pin):
        """
        Registers API as a new mobile device

        Args:
            token (:class:`str`): Token
            symbol (:class:`str`): Symbol
            pin (:class:`str`): PIN code

        Returns:
            :class:`vulcan.Certificate`: Generated certificate, that you need to save
        """
        return Certificate.get(token, symbol, pin)

    def get_students(self):
        """
        Yields students that are assigned to the account

        Yields:
            :class:`vulcan.Student`
        """
        return Student.get(self._api)

    def set_student(self, student):
        """
        Sets the default student

        Args:
            student (:class:`vulcan.Student`): Student from :func:`vulcan.Vulcan.get_students`
        """
        self._api.set_student(student)

    def get_grades(self):
        """
        Fetches student grades

        Yields:
            :class:`vulcan.Grade`
        """
        return Grade.get(self._api)

    def get_lessons(self, date=None):
        """
        Fetches lessons from the given date

        Args:
            date (:class:`datetime.date`): Date, from which to fetch lessons, if not provided
                it's using the today date

        Yields:
            :class:`vulcan.Lesson`
        """
        return Lesson.get(self._api, date)

    def get_exams(self, date=None):
        """
        Fetches exams from the given date

        Args:
            date (:class:`datetime.date`): Date, from which to fetch exams, if not provided
                it's using the today date

        Yields:
            :class:`vulcan.Exam`
        """
        return Exam.get(self._api, date)

    def get_homework(self, date=None):
        """
        Fetches homework from the given date

        Args:
            date (:class:`datetime.date`): Date, from which to fetch exams, if not provided
                it's using the today date

        Yields:
            :class:`vulcan.Homework`
        """
        return Homework.get(self._api, date)
