# -*- coding: utf-8 -*-
from typing import List

from ._api import Api
from ._data import VulcanData
from ._utils import log
from .model import Student


class Vulcan:
    """Vulcan API client.

    Contains methods for getting/setting the current student and for
    setting the logging level. All data is fetched from an instance
    of the :class:`~vulcan._data.VulcanData`, accessible
    using the ``data`` variable.

    :var `~vulcan._data.VulcanData` ~.data: the data client
    """

    def __init__(self, keystore, account, logging_level: int = None):
        self._api = Api(keystore, account)
        self._students = []
        self.data = VulcanData(self._api)

        if logging_level:
            Vulcan.set_logging_level(logging_level)

    async def __aenter__(self):
        await self._api.open()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._api.close()

    async def close(self):
        await self._api.close()

    async def select_student(self):
        """Load a list of students associated with the account.
        Set the first available student as default for the API.
        """
        students = await self.get_students()
        self.student = students[0] if len(students) > 0 else None

    @staticmethod
    def set_logging_level(logging_level: int):
        """Set the API logging level.

        :param int logging_level: logging level from `logging` module
        """
        log.setLevel(logging_level)

    async def get_students(self, cached=True) -> List[Student]:
        """Gets students assigned to this account.

        :param bool cached: whether to allow returning the cached list
        :rtype: List[:class:`~vulcan.model.Student`]
        """
        if self._students and cached:
            return self._students
        self._students = await Student.get(self._api)
        return self._students

    @property
    def student(self) -> Student:
        """Gets/sets the currently selected student.

        :rtype: :class:`~vulcan.model.Student`
        """
        return self._api.student

    @student.setter
    def student(self, value: Student):
        """Changes the currently selected student.

        :param value: the student to select
        :type value: :class:`~vulcan.model.Student`
        """
        self._api.student = value
