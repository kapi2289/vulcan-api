# -*- coding: utf-8 -*-

from related import immutable, StringField, IntegerField, TimeField
from ..._utils import TIME_FORMAT_H_M

from ._serializable import Serializable


@immutable
class TimeSlot(Serializable):
    """Lesson time (start-end range)

    :var int ~.id: Lesson time ID
    :var `datetime.time` ~.from_: Lesson start time
    :var `datetime.time` ~.to: Lesson end time
    :var str ~.displayed_time: lesson's displayed time
    :var int ~.position: Lesson position
    """

    id: int = IntegerField(key="Id")
    from_: TimeField = TimeField(key="Start", formatter=TIME_FORMAT_H_M)
    to: TimeField = TimeField(key="End", formatter=TIME_FORMAT_H_M)
    displayed_time: str = StringField(key="Display")
    position: int = IntegerField(key="Position")
