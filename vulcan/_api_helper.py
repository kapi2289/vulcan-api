# -*- coding: utf-8 -*-
from datetime import date, datetime
from enum import Enum, unique

from ._endpoints import (
    DATA_BY_MESSAGEBOX,
    DATA_BY_PERIOD,
    DATA_BY_PERSON,
    DATA_BY_PUPIL,
    DATA_ROOT,
)


@unique
class FilterType(Enum):
    BY_PUPIL = 0
    BY_PERSON = 1
    BY_PERIOD = 2
    BY_MESSAGEBOX = 3
    BY_LOGIN_ID = None

    def get_endpoint(self):
        if self == FilterType.BY_PUPIL:
            return DATA_BY_PUPIL
        elif self == FilterType.BY_PERSON:
            return DATA_BY_PERSON
        elif self == FilterType.BY_PERIOD:
            return DATA_BY_PERIOD
        elif self == FilterType.BY_MESSAGEBOX:
            return DATA_BY_MESSAGEBOX
        else:
            return None


class ApiHelper:
    def __init__(self, api):
        self._api = api

    async def get_list(
        self,
        endpoint: str,
        filter_type: FilterType,
        deleted: bool = False,
        date_from: date = None,
        date_to: date = None,
        last_sync: datetime = None,
        message_box: str = None,
        folder: int = None,
        params: dict = None,
        **kwargs,
    ) -> list:
        if not self._api.student:
            raise AttributeError("No student is selected.")
        if deleted:
            raise NotImplementedError(
                "Getting deleted data IDs is not implemented yet."
            )
        if filter_type and filter_type != FilterType.BY_LOGIN_ID:
            url = f"{DATA_ROOT}/{endpoint}/{filter_type.get_endpoint()}"
        else:
            url = f"{DATA_ROOT}/{endpoint}"
        query = {}
        account = self._api.account
        student = self._api.student
        period = self._api.period

        if filter_type == FilterType.BY_PUPIL:
            query["unitId"] = student.unit.id
            query["pupilId"] = student.pupil.id
            query["periodId"] = period.id
        elif filter_type in [FilterType.BY_PERSON, FilterType.BY_LOGIN_ID]:
            query["loginId"] = account.login_id
        elif filter_type == FilterType.BY_PERIOD:
            query["periodId"] = period.id
            query["pupilId"] = student.pupil.id
        elif filter_type == FilterType.BY_MESSAGEBOX:
            if not message_box:
                raise AttributeError("No message box specified.")
            query["box"] = message_box

        if date_from:
            query["dateFrom"] = date_from.strftime("%Y-%m-%d")
        if date_to:
            query["dateTo"] = date_to.strftime("%Y-%m-%d")
        if folder is not None:
            query["folder"] = folder

        query["lastId"] = "-2147483648"  # don't ask, it's just Vulcan
        query["pageSize"] = 500
        query["lastSyncDate"] = (last_sync or datetime(1970, 1, 1, 0, 0, 0)).strftime(
            "%Y-%m-%d %H:%m:%S"
        )

        if params:
            query.update(params)
        return await self._api.get(url, query, **kwargs)

    async def get_object(
        self, cls, endpoint: str, query: dict = None, **kwargs
    ) -> object:
        url = f"{DATA_ROOT}/{endpoint}"
        data = await self._api.get(url, query, **kwargs)
        return cls.load(data)
