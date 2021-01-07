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
from ..model import (
    Serializable,
    DateTime,
    Teacher,
    Subject,
    TeamClass,
    TeamVirtual,
    TimeSlot,
)
from ..._utils import TIME_FORMAT_H_M


@immutable
class LessonRoom(Serializable):
    """Lesson room

    :var int ~.id: Lesson room ID
    :var str ~.code: Classroom code
    """

    id: int = IntegerField(key="Id")
    code: str = StringField(key="Code")


@immutable
class Lesson(Serializable):
    """A lesson.

    :var int ~.id: lesson's ID
    :var `~vulcan.hebe.model.DateTime` ~.date: lesson's date
    :var `~vulcan.hebe.model.TimeSlot` ~.time: lesson's time
    :var `~vulcan.hebe.data.LessonRoom` ~.room: Classroom, in which is the lesson
    :var `~vulcan.hebe.model.Teacher` ~.teacher: Teacher of the lesson
    :var `~vulcan.hebe.model.Teacher` ~.second_teacher: Seccond teacher of the lesson
    :var `~vulcan.hebe.model.Subject` ~.subject: Subject on the lesson
    :var str ~.event: An event happening during this lesson
    :var str ~.changes: Lesson changes
    :var `~vulcan.hebe.model.TeamClass` ~.team_class: The class that has the lesson
    :var str ~.pupil_alias: Pupil Alias
    :var `~vulcan.hebe.model.TeamVirtual` ~.group: Group, that has the lesson
    :var bool ~.visible: Lesson visibility (whether the timetable applies to the given student)
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
    changes: str = StringField(key="Change", required=False)
    team_class: TeamClass = ChildField(TeamClass, key="Clazz", required=False)
    pupil_alias: str = StringField(key="PupilAlias", required=False)
    group: TeamVirtual = ChildField(TeamVirtual, key="Distribution", required=False)
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
