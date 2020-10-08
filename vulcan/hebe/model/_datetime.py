# -*- coding: utf-8 -*-

from related import immutable, IntegerField, DateField, TimeField
from ._serializable import Serializable


@immutable
class DateTime(Serializable):
    timestamp = IntegerField(key="Timestamp")
    date = DateField(key="Date")
    time = TimeField(key="Time")
