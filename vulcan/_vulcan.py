# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ._api import Api
from ._attendance import Attendance
from ._certificate import Certificate
from ._exam import Exam
from ._grade import Grade
from ._homework import Homework
from ._lesson import Lesson
from ._message import Message
from ._notice import Notice
from ._student import Student
from ._utils import log


class Vulcan:
    """Logs in to the e-register using generated certificate.

    :param certificate: Generated certificate using :func:`vulcan.Vulcan.register`
    :type certificate: dict or :class:`vulcan._certificate.Certificate`
    """

    def __init__(self, certificate, logging_level=None):
        self._api = Api(certificate)

        if logging_level:
            Vulcan.set_logging_level(logging_level)

        self.students = self.get_students()
        self.set_student(next(self.students))

    @staticmethod
    def set_logging_level(logging_level):
        """Sets the default logging level

        :param int logging_level: Logging level constant from `logging` module
        """

        log.setLevel(logging_level)

    @staticmethod
    def register(token, symbol, pin, name="Vulcan API"):
        """Registers API as a new mobile device

        :param str token: Token
        :param str symbol: Symbol
        :param str pin: PIN code
        :param str name: Device name, defaults to "Vulcan API"
        :returns: Generated certificate, use `json` property to save it to a file
        :rtype: :class:`vulcan._certificate.Certificate`

        """
        return Certificate.get(token, symbol, pin, str(name))

    def get_students(self):
        """Fetches students that are assigned to the account

        :rtype: Iterator[:class:`vulcan._student.Student`]
        """
        return Student.get(self._api)

    def set_student(self, student):
        """Sets the default student

        :param `vulcan._student.Student` student: Student from :func:`vulcan.Vulcan.get_students`
        """
        self._api.set_student(student)

    @property
    def dictionaries(self):
        """Dictionaries, that include i.a. teachers

        :rtype: :class:`vulcan._dictionaries.Dictionaries`
        """
        return self._api.dict

    def get_grades(self):
        """
        Fetches student grades

        :rtype: Iterator[:class:`vulcan._grade.Grade`]
        """
        return Grade.get(self._api)

    def get_lessons(self, date_from=None, date_to=None):
        """Fetches lessons from the given date

        :param `datetime.date` date_from: Date, from which to fetch lessons, if not provided
            it's using the today date (Default value = None)
        :param `datetime.date` date_to: Date, to which to fetch lessons, if not provided
            it's using the `date_from` date (Default value = None)

        :rtype: Iterator[:class:`vulcan._lesson.Lesson`]
        """
        return Lesson.get(self._api, date_from, date_to)

    def get_exams(self, date_from=None, date_to=None):
        """Fetches exams from the given date

        :param `datetime.date` date_from: Date, from which to fetch lessons, if not provided
            it's using the today date (Default value = None)
        :param `datetime.date` date_to: Date, to which to fetch lessons, if not provided
            it's using the `date_from` date (Default value = None)

        :rtype: Iterator[:class:`vulcan._exam.Exam`]
        """
        return Exam.get(self._api, date_from, date_to)

    def get_homework(self, date_from=None, date_to=None):
        """Fetches homework from the given date

        :param `datetime.date` date_from: Date, from which to fetch lessons, if not provided
                it's using the today date (Default value = None)
        :param `datetime.date` date_to: Date, to which to fetch lessons, if not provided
                it's the `date_from` date (Default value = None)

        :rtype: Iterator[:class:`vulcan._homework.Homework`]
        """
        return Homework.get(self._api, date_from, date_to)

    def get_notices(self):
        """Fetches notices from the current semester (period)

        :rtype: Iterator[:class:`vulcan._notice.Notice`]
        """
        return Notice.get(self._api)

    def get_attendance(self, date_from=None, date_to=None):
        """Fetches attendance from the given date

        :param `datetime.date` date_from: Date, from which to fetch lessons, if not provided
            it's using the today date (Default value = None)
        :param `datetime.date` date_to: Date, to which to fetch lessons, if not provided
            it's the `date_from` date (Default value = None)

        :rtype: Iterator[:class:`vulcan._attendance.Attendance`]
        """
        return Attendance.get(self._api, date_from, date_to)

    def get_messages(self, date_from=None, date_to=None):
        """Fetches messages from the given date

        :param `datetime.date` date_from: Date, from which to fetch messages, if not provided
            it's using the semester (period) start date (Default value = None)
        :param `datetime.date` date_to: Date, to which to fetch messages, if not provided
            it's using the semester (period) end date (Default value = None)

        :rtype: Iterator[:class:`vulcan._message.Message`]
        """
        return Message.get(self._api, date_from, date_to)
