# -*- coding: utf-8 -*-

from datetime import datetime

from related import immutable, IntegerField, DateField, TimeField

from ._serializable import Serializable


@immutable
class DateTime(Serializable):
    timestamp = IntegerField(key="Timestamp")
    date = DateField(key="Date")
    time = TimeField(key="Time")

    @property
    def date_time(self):
        """Combine the date and time of this object.

        :rtype: :class:`datetime.datetime`
        """
        return datetime.combine(self.date, self.time)
