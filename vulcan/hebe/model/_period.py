# -*- coding: utf-8 -*-

from related import immutable, IntegerField, BooleanField, ChildField

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
    :var `~vulcan.hebe.model.DateTime` ~.start: the period start datetime
    :var `~vulcan.hebe.model.DateTime` ~.end: the period end datetime
    """

    id = IntegerField(key="Id")
    level = IntegerField(key="Level")
    number = IntegerField(key="Number")
    current = BooleanField(key="Current")
    last = BooleanField(key="Last")
    start = ChildField(DateTime, key="Start")
    end = ChildField(DateTime, key="End")
