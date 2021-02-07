# -*- coding: utf-8 -*-
from datetime import date

from related import DateField, IntegerField, immutable

from .._endpoints import DATA_LUCKY_NUMBER
from ..model import Serializable


@immutable
class LuckyNumber(Serializable):
    """A lucky number for the specified date.

    :var `datetime.date` ~.date: lucky number date
    :var int ~.number: the lucky number
    """

    date: date = DateField(key="Day")
    number: int = IntegerField(key="Number")

    @classmethod
    async def get(cls, api, day: date, **kwargs) -> "LuckyNumber":
        """
        :rtype: :class:`~vulcan.data.LuckyNumber`
        """
        return await api.helper.get_object(
            LuckyNumber,
            DATA_LUCKY_NUMBER,
            query={
                "constituentId": api.student.school.id,
                "day": day.strftime("%Y-%m-%d"),
            },
            **kwargs
        )
