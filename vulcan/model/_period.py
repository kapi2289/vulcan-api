# -*- coding: utf-8 -*-

from related import BooleanField, ChildField, IntegerField, immutable

from ._datetime import DateTime
from ._serializable import Serializable


@immutable
class Period(Serializable):
    """A school year period.

    :var int ~.id: the period ID
    :var int ~.level: a grade/level number
    :var int ~.number: number of the period in the school year
    :var bool ~.current: whether the period is currently ongoing
    :var bool ~.last: whether the period is last in the school year
    :var `~vulcan.model.DateTime` ~.start: the period start datetime
    :var `~vulcan.model.DateTime` ~.end: the period end datetime
    """

    id: int = IntegerField(key="Id")
    level: int = IntegerField(key="Level")
    number: int = IntegerField(key="Number")
    current: bool = BooleanField(key="Current")
    last: bool = BooleanField(key="Last")
    start: DateTime = ChildField(DateTime, key="Start")
    end: DateTime = ChildField(DateTime, key="End")
