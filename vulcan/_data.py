# -*- coding: utf-8 -*-
from datetime import date, datetime
from typing import AsyncIterator, List, Union

from ._api import Api
from .data import (
    Addressbook,
    Attendance,
    ChangedLesson,
    Exam,
    Grade,
    Homework,
    Lesson,
    LuckyNumber,
    Message,
)
from .model import DateTime


class VulcanData:
    """A data client for the API.

    Contains methods for getting all data objects, some in
    form of a list, others as an object. All the methods
    are asynchronous. Additionally, the list getting methods
    return an `AsyncIterator` of the items.

    The data client shall not be constructed outside of the main
    API class.
    """

    def __init__(self, api: Api):
        self._api = api

    async def get_time(self) -> DateTime:
        """Gets the current server time.

        :rtype: :class:`~vulcan.model.DateTime`
        """
        return await DateTime.get(self._api)

    async def get_lucky_number(self, day: date = None) -> LuckyNumber:
        """Gets the lucky number for the specified date.

        :param `datetime.date` day: date of the lucky number to get.
            Defaults to ``None`` (today).
        :rtype: :class:`~vulcan.data.LuckyNumber`
        """
        return await LuckyNumber.get(self._api, day or date.today())

    async def get_addressbook(
        self, **kwargs
    ) -> Union[AsyncIterator[Addressbook], List[int]]:
        """Yields the addressbook.

        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Addressbook`], List[int]]
        """
        return Addressbook.get(self._api, **kwargs)

    async def get_messages(
        self, last_sync: datetime = None, folder=1, **kwargs
    ) -> Union[AsyncIterator[Message], List[int]]:
        """Yields messages received by the currently registered account.

        :param `datetime.datetime` last_sync: date of the last sync,
            gets only the objects updated since this date
        :param int folder: message folder: 1 - received; 2 - sent; 3 - deleted
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Message`], List[int]]
        """
        return Message.get(self._api, last_sync, folder, **kwargs)

    async def get_grades(
        self, last_sync: datetime = None, deleted=False, **kwargs
    ) -> Union[AsyncIterator[Grade], List[int]]:
        """Yields the student's grades.

        :param `datetime.datetime` last_sync: date of the last sync,
            gets only the objects updated since this date
        :param bool deleted: whether to only get the deleted item IDs
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Grade`], List[int]]
        """
        return Grade.get(self._api, last_sync, deleted, **kwargs)

    async def get_exams(
        self, last_sync: datetime = None, deleted=False, **kwargs
    ) -> Union[AsyncIterator[Grade], List[int]]:
        """Yields the student's exams.

        :param `datetime.datetime` last_sync: date of the last sync,
            gets only the objects updated since this date
        :param bool deleted: whether to only get the deleted item IDs
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Exam`], List[int]]
        """
        return Exam.get(self._api, last_sync, deleted, **kwargs)

    async def get_homework(
        self, last_sync: datetime = None, deleted=False, **kwargs
    ) -> Union[AsyncIterator[Homework], List[int]]:
        """Yields the student's homework.

        :param `datetime.datetime` last_sync: date of the last sync,
            gets only the objects updated since this date
        :param bool deleted: whether to only get the deleted item IDs
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Homework`], List[int]]
        """
        return Homework.get(self._api, last_sync, deleted, **kwargs)

    async def get_lessons(
        self,
        last_sync: datetime = None,
        deleted=False,
        date_from=None,
        date_to=None,
        **kwargs,
    ) -> Union[AsyncIterator[Lesson], List[int]]:
        """Yields the student's lessons.

        :param `datetime.datetime` last_sync: date of the last sync,
            gets only the objects updated since this date
        :param bool deleted: whether to only get the deleted item IDs
        :param `datetime.date` date_from: Date, from which to fetch lessons, if not provided
            it's using the today date (Default value = None)
        :param `datetime.date` date_to: Date, to which to fetch lessons, if not provided
            it's using the `date_from` date (Default value = None)
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Lesson`], List[int]]
        """
        return Lesson.get(self._api, last_sync, deleted, date_from, date_to, **kwargs)

    async def get_changed_lessons(
        self,
        last_sync: datetime = None,
        deleted=False,
        date_from=None,
        date_to=None,
        **kwargs,
    ) -> Union[AsyncIterator[ChangedLesson], List[int]]:
        """Yields the student's changed lessons.

        :param `datetime.datetime` last_sync: date of the last sync,
            gets only the objects updated since this date
        :param bool deleted: whether to only get the deleted item IDs
        :param `datetime.date` date_from: Date, from which to fetch lessons, if not provided
            it's using the today date (Default value = None)
        :param `datetime.date` date_to: Date, to which to fetch lessons, if not provided
            it's using the `date_from` date (Default value = None)
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.ChangedLesson`], List[int]]
        """
        return ChangedLesson.get(
            self._api, last_sync, deleted, date_from, date_to, **kwargs
        )

    async def get_attendance(
        self,
        last_sync: datetime = None,
        deleted=False,
        date_from=None,
        date_to=None,
        **kwargs,
    ) -> Union[AsyncIterator[Attendance], List[int]]:
        """Fetches attendance from the given date

        :param `datetime.datetime` last_sync: date of the last sync,
            gets only the objects updated since this date
        :param bool deleted: whether to only get the deleted item IDs
        :param `datetime.date` date_from: Date, from which to fetch attendance, if not provided
            it's using the today date (Default value = None)
        :param `datetime.date` date_to: Date, to which to fetch attendance, if not provided
            it's using the `date_from` date (Default value = None)
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Attendance`], List[int]]
        """
        return Attendance.get(
            self._api, last_sync, deleted, date_from, date_to, **kwargs
        )
