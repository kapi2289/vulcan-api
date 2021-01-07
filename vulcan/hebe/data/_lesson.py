# -*- coding: utf-8 -*-
from typing import Union, AsyncIterator, List
import datetime
from related import (
    immutable,
    IntegerField,
    StringField,
    ChildField,
    BooleanField,
    SequenceField,
    TimeField,
)

from .._api_helper import FilterType
from .._endpoints import DATA_TIMETABLE
from ..model import Serializable, DateTime, Teacher, Subject, TeamClass, TeamVirtual
from ..._utils import TIME_FORMAT_H_M, sort_and_filter_dates


@immutable
class LessonTime(Serializable):
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


@immutable
class LessonRoom(Serializable):
    """Lesson room

    :var int ~.id: Lesson room ID
    :var str ~.code: Classroom code
    """

    id: int = IntegerField(key="Id")
    code: str = StringField(key="Code")


@immutable
class LessonGroup(Serializable):
    """Lesson time (start-end range)

    :var int ~.id: Group ID
    :var str ~.key: Lesson's group key (UUID)
    :var str ~.shortcut: Group shortcut
    :var str ~.name: Group full name
    :var str ~.part_type: Group sorting type (eg. gender or advancement level)
    """

    id: int = IntegerField(key="Id")
    key: str = StringField(key="Key")
    shortcut: str = StringField(key="Shortcut")
    name: str = StringField(key="Name")
    part_type: str = StringField(key="PartType")


@immutable
class Lesson(Serializable):
    """A lesson.

    :var int ~.id: lesson's ID
    :var `~vulcan.hebe.model.DateTime` ~.date: lesson's date
    :var `~vulcan.hebe.data.LessonTime` ~.time: lesson's time
    :var `~vulcan.hebe.data.LessonRoom` ~.room: Classroom, in which is the lesson
    :var `~vulcan.hebe.model.Teacher` ~.teacher: Teacher of the lesson
    :var `~vulcan.hebe.model.Teacher` ~.second_teacher: Seccond teacher of the lesson
    :var `~vulcan.hebe.model.Subject` ~.subject: Subject on the lesson
    :var str ~.event: An event happening during this lesson
    :var str ~.changes: Lesson changes
    :var `~vulcan.hebe.model.TeamClass` ~.team_class: The class that has the lesson
    :var str ~.pupil_alias: Pupil Alias
    :var `~vulcan.hebe.data.LessonGroup` ~.group: Group, that has the lesson
    :var bool ~.visible: Lesson visibility (whether the timetable applies to the given student)
    """

    id: int = IntegerField(key="Id", required=False)
    date: DateTime = ChildField(DateTime, key="Date", required=False)
    time: LessonTime = ChildField(LessonTime, key="TimeSlot", required=False)
    room: LessonRoom = ChildField(LessonRoom, key="Room", required=False)
    teacher: Teacher = ChildField(Teacher, key="TeacherPrimary", required=False)
    second_teacher: Teacher = ChildField(
        Teacher, key="TeacherSecondary", required=False
    )
    subject: Subject = ChildField(Subject, key="Subject", required=False)
    event: str = StringField(key="Event", required=False)
    changes: str = StringField(key="Change", required=False)
    team_class: TeamClass = ChildField(TeamClass, key="Clazz", required=False)
    pupil_alias: str = StringField(key="PupilAlias", required=False)
    group: LessonGroup = ChildField(LessonGroup, key="Distribution", required=False)
    visible = BooleanField(key="Visible", required=False)

    @classmethod
    async def get(
        cls, api, last_sync, deleted, date_from, date_to, **kwargs
    ) -> Union[AsyncIterator["Lesson"], List[int]]:
        if date_from == None:
            date_from = datetime.date.today()
        if date_to == None:
            date_to = date_from
        date_to = date_to + datetime.timedelta(
            days=1
        )  # Vulcan requires the date_to to be one greater the date it is supposed to be
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.hebe.data.Lesson`], List[int]]
        """
        data = await api.helper.get_list(
            DATA_TIMETABLE,
            FilterType.BY_PUPIL,
            deleted=deleted,
            date_from=date_from,
            date_to=date_to,
            last_sync=last_sync,
            **kwargs
        )

        for lesson in data:
            yield Lesson.load(lesson)
