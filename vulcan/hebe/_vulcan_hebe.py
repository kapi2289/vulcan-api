# -*- coding: utf-8 -*-
from typing import List

from ._api import Api
from ._utils_hebe import log
from .model import Student


class VulcanHebe:
    def __init__(self, keystore, account, logging_level: int = None):
        self._api = Api(keystore, account)
        self._students = []
        self._student = None

        if logging_level:
            VulcanHebe.set_logging_level(logging_level)

    async def __aenter__(self):
        await self._api.open()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._api.close()

    async def close(self):
        await self._api.close()

    async def select_student(self):
        students = await self.get_students()
        self._student = students[-1]

    @staticmethod
    def set_logging_level(logging_level: int):
        """Set the API logging level.

        :param int logging_level: logging level from `logging` module
        """
        log.setLevel(logging_level)

    async def get_students(self, cached=True):
        """Gets students assigned to this account.

        :param bool cached: whether to allow returning the cached list
        :rtype: List[:class:`~vulcan.hebe.model.Student`]
        """
        if self._students and cached:
            return self._students
        self._students = await Student.get(self._api)
        return self._students

    @property
    def student(self):
        """Returns the currently selected student.

        :rtype: :class:`~vulcan.hebe.model.Student`
        """
        return self._student

    @student.setter
    def student(self, value):
        """Changes the currently selected student.

        :param value: the student to select
        :type value: :class:`~vulcan.hebe.model.Student`
        """
        self._student = value
        self._api.set_student(value)
