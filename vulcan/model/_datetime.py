# -*- coding: utf-8 -*-

from datetime import date, datetime, time

from related import DateField, IntegerField, TimeField, immutable

from .._endpoints import DATA_INTERNAL_TIME
from ._serializable import Serializable


@immutable
class DateTime(Serializable):
    """A date-time object used for representing points in time.

    :var int ~.timestamp: number of millis since the Unix epoch
    :var `datetime.date` ~.date: a date object
    :var `datetime.time` ~.time: a time object
    """

    timestamp: int = IntegerField(key="Timestamp")
    date: date = DateField(key="Date")
    time: time = TimeField(key="Time")

    @property
    def date_time(self) -> datetime:
        """Combine the date and time of this object.

        :rtype: :class:`datetime.datetime`
        """
        return datetime.combine(self.date, self.time)

    def __str__(self) -> str:
        return self.date_time.strftime("%Y-%m-%d %H:%m:%S")

    @classmethod
    async def get(cls, api, **kwargs) -> "DateTime":
        """
        :rtype: :class:`~vulcan.model.DateTime`
        """
        return await api.helper.get_object(DateTime, DATA_INTERNAL_TIME, *kwargs)
