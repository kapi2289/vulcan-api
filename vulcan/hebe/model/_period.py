# -*- coding: utf-8 -*-

from related import immutable, IntegerField, BooleanField, ChildField
from ._serializable import Serializable
from ._datetime import DateTime


@immutable
class Period(Serializable):
    id = IntegerField(key="Id")
    level = IntegerField(key="Level")
    number = IntegerField(key="Number")
    current = BooleanField(key="Current")
    last = BooleanField(key="Last")
    start = ChildField(DateTime, key="Start")
    end = ChildField(DateTime, key="End")
