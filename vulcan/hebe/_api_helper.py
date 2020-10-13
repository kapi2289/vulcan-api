# -*- coding: utf-8 -*-
from datetime import datetime, date
from enum import Enum, unique
from typing import Iterator

from ._endpoints import DATA_BY_PERSON, DATA_BY_PUPIL, DATA_BY_PERIOD, DATA_ROOT


@unique
class FilterType(Enum):
    BY_PUPIL = 0
    BY_PERSON = 1
    BY_PERIOD = 2

    def get_endpoint(self):
        if self == FilterType.BY_PUPIL:
            return DATA_BY_PUPIL
        elif self == FilterType.BY_PERSON:
            return DATA_BY_PERSON
        elif self == FilterType.BY_PERIOD:
            return DATA_BY_PERIOD
        else:
            return None


class ApiHelper:
    def __init__(self, api):
        self._api = api

    async def get_list(
        self,
        cls,
        endpoint: str,
        filter_type: FilterType,
        deleted: bool = False,
        date_from: date = None,
        date_to: date = None,
        last_sync: datetime = None,
        params: dict = None,
    ) -> Iterator:
        if deleted:
            raise NotImplementedError(
                "Getting deleted data IDs is not implemented yet."
            )

        if filter_type:
            url = "{}/{}/{}".format(DATA_ROOT, endpoint, filter_type.get_endpoint())
        else:
            url = "{}/{}".format(DATA_ROOT, endpoint)
        query = {}
        account = self._api.account
        student = self._api.student
        period = self._api.period

        if filter_type == FilterType.BY_PUPIL:
            query["unitId"] = student.unit.id
            query["pupilId"] = student.pupil.id
            query["periodId"] = period.id
        elif filter_type == FilterType.BY_PERSON:
            query["loginId"] = account.login_id
        elif filter_type == FilterType.BY_PERIOD:
            query["periodId"] = period.id
            query["pupilId"] = student.pupil.id
        if params:
            query.update(params)
        # query.update({
        #     "lastSyncDate": (last_sync or datetime.utcnow()).strftime("%Y-%m-%d %H:%m:%S")
        # })

        data = await self._api.get(url, query)
        return (cls.load(item) for item in data)
