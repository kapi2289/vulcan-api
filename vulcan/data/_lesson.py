# -*- coding: utf-8 -*-
import datetime
from typing import AsyncIterator, List, Union

from related import BooleanField, ChildField, IntegerField, StringField, immutable

from .._api_helper import FilterType
from .._endpoints import DATA_TIMETABLE, DATA_TIMETABLE_CHANGES
from ..model import (
    DateTime,
    Serializable,
    Subject,
    Teacher,
    TeamClass,
    TeamVirtual,
    TimeSlot,
)


@immutable
class LessonRoom(Serializable):
    """Lesson room

    :var int ~.id: lesson room ID
    :var str ~.code: classroom code
    """

    id: int = IntegerField(key="Id")
    code: str = StringField(key="Code")


@immutable
class LessonChanges(Serializable):
    """Lesson changes

    :var int ~.id: lesson change ID
    :var int ~.type: lesson change type
    :var bool ~.code: team separation
    """

    id: int = IntegerField(key="Id")
    type: int = IntegerField(key="Type")
    separation: bool = BooleanField(key="Separation")


@immutable
class Lesson(Serializable):
    """A lesson.

    :var int ~.id: lesson's ID
    :var `~vulcan.model.DateTime` ~.date: lesson's date
    :var `~vulcan.model.TimeSlot` ~.time: lesson's time
    :var `~vulcan.data.LessonRoom` ~.room: classroom, in which is the lesson
    :var `~vulcan.model.Teacher` ~.teacher: teacher of the lesson
    :var `~vulcan.model.Teacher` ~.second_teacher: second teacher of the lesson
    :var `~vulcan.model.Subject` ~.subject: subject on the lesson
    :var str ~.event: an event happening during this lesson
    :var `~vulcan.data.LessonChanges` ~.changes: lesson changes
    :var `~vulcan.model.TeamClass` ~.team_class: the class that has the lesson
    :var str ~.pupil_alias: pupil alias
    :var `~vulcan.model.TeamVirtual` ~.group: group, that has the lesson
    :var bool ~.visible: lesson visibility (whether the timetable applies to the given student)
    """

    id: int = IntegerField(key="Id", required=False)
    date: DateTime = ChildField(DateTime, key="Date", required=False)
    time: TimeSlot = ChildField(TimeSlot, key="TimeSlot", required=False)
    room: LessonRoom = ChildField(LessonRoom, key="Room", required=False)
    teacher: Teacher = ChildField(Teacher, key="TeacherPrimary", required=False)
    second_teacher: Teacher = ChildField(
        Teacher, key="TeacherSecondary", required=False
    )
    subject: Subject = ChildField(Subject, key="Subject", required=False)
    event: str = StringField(key="Event", required=False)
    changes: LessonChanges = ChildField(LessonChanges, key="Change", required=False)
    team_class: TeamClass = ChildField(TeamClass, key="Clazz", required=False)
    pupil_alias: str = StringField(key="PupilAlias", required=False)
    group: TeamVirtual = ChildField(TeamVirtual, key="Distribution", required=False)
    visible: bool = BooleanField(key="Visible", required=False)

    @classmethod
    async def get(
        cls, api, last_sync, deleted, date_from, date_to, **kwargs
    ) -> Union[AsyncIterator["Lesson"], List[int]]:
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Lesson`], List[int]]
        """
        if date_from is None:
            date_from = datetime.date.today()
        if date_to is None:
            date_to = date_from
        date_to = date_to + datetime.timedelta(
            days=1
        )  # Vulcan requires the date_to to be one greater the date it is supposed to be
        data = await api.helper.get_list(
            DATA_TIMETABLE,
            FilterType.BY_PUPIL,
            deleted=deleted,
            date_from=date_from,
            date_to=date_to,
            last_sync=last_sync,
            **kwargs,
        )

        for lesson in data:
            yield Lesson.load(lesson)


@immutable
class ChangedLesson(Serializable):
    """Changed lesson.

    :var int ~.id: changed lesson's ID
    :var int ~.unit_id: unit ID
    :var int ~.schedule_id: normal lesson's ID
    :var `~vulcan.model.DateTime` ~.lesson_date: lesson's date
    :var `~vulcan.model.DateTime` ~.change_date: change date
    :var `~vulcan.model.TimeSlot` ~.time: lesson's time
    :var str ~.note: change note
    :var str ~.reason: change reason
    :var `~vulcan.data.LessonRoom` ~.room: classroom, in which is the lesson
    :var `~vulcan.model.Teacher` ~.teacher: teacher of the lesson
    :var `~vulcan.model.Teacher` ~.second_teacher: second teacher of the lesson
    :var `~vulcan.model.Subject` ~.subject: subject on the lesson
    :var str ~.event: an event happening during this lesson
    :var `~vulcan.data.LessonChanges` ~.changes: lesson changes
    :var `~vulcan.model.TeamClass` ~.team_class: the class that has the lesson
    :var `~vulcan.model.TeamVirtual` ~.group: group, that has the lesson
    """

    id: int = IntegerField(key="Id", required=False)
    unit_id: int = IntegerField(key="UnitId", required=False)
    schedule_id: int = IntegerField(key="'ScheduleId': ", required=False)
    lesson_date: DateTime = ChildField(DateTime, key="LessonDate", required=False)
    note: str = StringField(key="Note", required=False)
    reason: str = StringField(key="Reason", required=False)
    time: TimeSlot = ChildField(TimeSlot, key="TimeSlot", required=False)
    room: LessonRoom = ChildField(LessonRoom, key="Room", required=False)
    teacher: Teacher = ChildField(Teacher, key="TeacherPrimary", required=False)
    second_teacher: Teacher = ChildField(
        Teacher, key="TeacherSecondary", required=False
    )
    subject: Subject = ChildField(Subject, key="Subject", required=False)
    event: str = StringField(key="Event", required=False)
    changes: LessonChanges = ChildField(LessonChanges, key="Change", required=False)
    change_date: DateTime = ChildField(DateTime, key="ChangeDate", required=False)
    team_class: TeamClass = ChildField(TeamClass, key="Clazz", required=False)
    group: TeamVirtual = ChildField(TeamVirtual, key="Distribution", required=False)

    @classmethod
    async def get(
        cls, api, last_sync, deleted, date_from, date_to, **kwargs
    ) -> Union[AsyncIterator["Lesson"], List[int]]:
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.ChangeLesson`], List[int]]
        """
        if date_from is None:
            date_from = datetime.date.today()
        if date_to is None:
            date_to = date_from
        date_to = date_to + datetime.timedelta(
            days=1
        )  # Vulcan requires the date_to to be one greater the date it is supposed to be
        data = await api.helper.get_list(
            DATA_TIMETABLE_CHANGES,
            FilterType.BY_PUPIL,
            deleted=deleted,
            date_from=date_from,
            date_to=date_to,
            last_sync=last_sync,
            **kwargs,
        )

        for lesson in data:
            yield ChangedLesson.load(lesson)
