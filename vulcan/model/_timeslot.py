# -*- coding: utf-8 -*-

from related import IntegerField, StringField, TimeField, immutable

from .._utils import TIME_FORMAT_H_M
from ._serializable import Serializable


@immutable
class TimeSlot(Serializable):
    """Lesson time (start-end range)

    :var int ~.id: lesson time ID
    :var `datetime.time` ~.from_: lesson start time
    :var `datetime.time` ~.to: lesson end time
    :var str ~.displayed_time: lesson's displayed time
    :var int ~.position: lesson position
    """

    id: int = IntegerField(key="Id")
    from_: TimeField = TimeField(key="Start", formatter=TIME_FORMAT_H_M)
    to: TimeField = TimeField(key="End", formatter=TIME_FORMAT_H_M)
    displayed_time: str = StringField(key="Display")
    position: int = IntegerField(key="Position")
