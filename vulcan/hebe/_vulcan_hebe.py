# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Union, AsyncIterator

from ._api import Api
from ._utils_hebe import log
from .data import Grade
from .model import Student, DateTime


class VulcanHebe:
    def __init__(self, keystore, account, logging_level: int = None):
        self._api = Api(keystore, account)
        self._students = []

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
        self.student = students[-1]

    @staticmethod
    def set_logging_level(logging_level: int):
        """Set the API logging level.

        :param int logging_level: logging level from `logging` module
        """
        log.setLevel(logging_level)

    async def get_students(self, cached=True) -> List[Student]:
        """Gets students assigned to this account.

        :param bool cached: whether to allow returning the cached list
        :rtype: List[:class:`~vulcan.hebe.model.Student`]
        """
        if self._students and cached:
            return self._students
        self._students = await Student.get(self._api)
        return self._students

    @property
    def student(self) -> Student:
        """Gets/sets the currently selected student.

        :rtype: :class:`~vulcan.hebe.model.Student`
        """
        return self._api.student

    @student.setter
    def student(self, value: Student):
        """Changes the currently selected student.

        :param value: the student to select
        :type value: :class:`~vulcan.hebe.model.Student`
        """
        self._api.student = value

    async def get_time(self) -> DateTime:
        """Gets the current server time.

        :rtype: :class:`~vulcan.hebe.model.DateTime`
        """
        return await DateTime.get(self._api)

    async def get_grades(
        self, last_sync: datetime = None, deleted=False, **kwargs
    ) -> Union[AsyncIterator[Grade], List[int]]:
        """Yields the student's grades.

        :param `datetime.datetime` last_sync: date of the last sync,
            gets only the objects updated since this date
        :param bool deleted: whether to only get the deleted item IDs
        :rtype: Union[AsyncIterator[:class:`~vulcan.hebe.data.Grade`], List[int]]
        """
        return Grade.get(self._api, last_sync, deleted, **kwargs)
