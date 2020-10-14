# -*- coding: utf-8 -*-

from datetime import datetime

from related import immutable, IntegerField, DateField, TimeField

from ._serializable import Serializable
from .._endpoints import DATA_INTERNAL_TIME


@immutable
class DateTime(Serializable):
    """A date-time object used for representing points in time.

    :var int ~.timestamp: number of millis since the Unix epoch
    :var `datetime.date` ~.date: a date object
    :var `datetime.time` ~.time: a time object
    """

    timestamp = IntegerField(key="Timestamp")
    date = DateField(key="Date")
    time = TimeField(key="Time")

    @property
    def date_time(self):
        """Combine the date and time of this object.

        :rtype: :class:`datetime.datetime`
        """
        return datetime.combine(self.date, self.time)

    def __str__(self):
        return self.date_time.strftime("%Y-%m-%d %H:%m:%S")

    @classmethod
    async def get(cls, api):
        return await api.helper.get_object(DateTime, DATA_INTERNAL_TIME)
