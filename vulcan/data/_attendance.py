# -*- coding: utf-8 -*-
import datetime
from typing import AsyncIterator, List, Union

from related import BooleanField, ChildField, IntegerField, StringField, immutable

from .._api_helper import FilterType
from .._endpoints import DATA_ATTENDANCE
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
class PresenceType(Serializable):
    """Presence type

    :var int ~.id: attendance ID
    :var str ~.name: attendance name
    :var str ~.symbol: attendance symbol
    :var int ~.category_id: attendance category ID
    :var str ~.category_name: attendance category name
    :var int ~.position: attendance position
    :var bool ~.presence: presence on lesson
    :var bool ~.absence: absence on lesson
    :var bool ~.exemption: exemption from lesson
    :var bool ~.late: is late for lesson
    :var bool ~.justified: justified absence
    :var bool ~.deleted: whether the entry is deleted
    """

    id = IntegerField(key="Id")
    name: str = StringField(key="Name")
    symbol: str = StringField(key="Symbol")
    category_id: int = IntegerField(key="CategoryId")
    category_name: str = StringField(key="CategoryName")
    position: int = IntegerField(key="Position")
    presence: bool = BooleanField(key="Presence")
    absence: bool = BooleanField(key="Absence")
    exemption: bool = BooleanField(key="LegalAbsence")
    late: bool = BooleanField(key="Late")
    justified: bool = BooleanField(key="AbsenceJustified")
    deleted: bool = BooleanField(key="Removed")


@immutable
class Attendance(Serializable):
    """Attendance.

    :var int ~.lesson_id: lesson ID
    :var int ~.id: attendance ID
    :var int ~.lesson_number: lesson number
    :var str ~.global_key: attendance global key
    :var int ~.lesson_class_id: lesson class ID
    :var str ~.global_key: lesson class global key
    :var bool ~.calculate_presence: does it count for absences
    :var bool ~.replacement: os it replaced
    :var `~vulcan.model.Subject` ~.subject: subject of the lesson
    :var str ~.topic: topic of the lesson
    :var `~vulcan.model.Teacher` ~.teacher: teacher of the lesson
    :var `~vulcan.model.Teacher` ~.second_teacher: second teacher of the lesson
    :var `~vulcan.model.Teacher` ~.main_teacher: pupil main teacher
    :var `~vulcan.model.TeamClass` ~.team_class: the class that had lesson
    :var str ~.class_alias: class short name
    :var `~vulcan.model.DateTime` ~.date: lesson's date
    :var `~vulcan.model.TimeSlot` ~.time: lesson's time
    :var `~vulcan.model.DateTime` ~.date_modified: attendance modification date, if not modified it is created date
    :var int ~.id: aux presence ID
    :var str ~.justification_status: attendance justification status
    :var `~vulcan.data.PresenceType` ~.presence_type: presence type
    :var str ~.note: attendance note
    :var str ~.public_resources: attendance public resources
    :var str ~.remote_resources: attendance remote resources
    :var `~vulcan.model.TeamVirtual` ~.group: group, that has the lesson
    :var bool ~.visible: attendance visibility

    """

    lesson_id: int = IntegerField(key="LessonId")
    id: int = IntegerField(key="Id")
    lesson_number: int = IntegerField(key="LessonNumber")
    global_key: str = StringField(key="GlobalKey")
    lesson_class_id: int = IntegerField(key="LessonClassId")
    lesson_class_global_key: str = StringField(key="LessonClassGlobalKey")
    calculate_presence: bool = BooleanField(key="CalculatePresence")
    replacement: bool = BooleanField(key="Replacement")
    subject: Subject = ChildField(Subject, key="Subject", required=False)
    topic: str = StringField(key="Topic", required=False)
    teacher: Teacher = ChildField(Teacher, key="TeacherPrimary", required=False)
    second_teacher: Teacher = ChildField(
        Teacher, key="TeacherSecondary", required=False
    )
    main_teacher: Teacher = ChildField(Teacher, key="TeacherMod", required=False)
    team_class: TeamClass = ChildField(TeamClass, key="Clazz", required=False)
    class_alias: str = StringField(key="GroupDefinition", required=False)
    date: DateTime = ChildField(DateTime, key="Day", required=False)
    time: TimeSlot = ChildField(TimeSlot, key="TimeSlot", required=False)
    date_modified: DateTime = ChildField(DateTime, key="DateModify", required=False)
    aux_presence_id: int = IntegerField(key="AuxPresenceId", required=False)
    justification_status: str = StringField(key="JustificationStatus", required=False)
    presence_type: PresenceType = ChildField(
        PresenceType, key="PresenceType", required=False
    )
    note: str = StringField(key="Note", required=False)
    public_resources: str = StringField(key="PublicResources", required=False)
    remote_resources: str = StringField(key="RemoteResources", required=False)
    group: TeamVirtual = ChildField(TeamVirtual, key="Distribution", required=False)
    visible = BooleanField(key="Visible", required=False)

    @classmethod
    async def get(
        cls, api, last_sync, deleted, date_from, date_to, **kwargs
    ) -> Union[AsyncIterator["Attendance"], List[int]]:
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Attendance`], List[int]]
        """
        if date_from is None:
            date_from = datetime.date.today()
        if date_to is None:
            date_to = date_from
        date_to = date_to + datetime.timedelta(
            days=1
        )  # Vulcan requires the date_to to be one greater the date it is supposed to be
        data = await api.helper.get_list(
            DATA_ATTENDANCE,
            FilterType.BY_PUPIL,
            deleted=deleted,
            date_from=date_from,
            date_to=date_to,
            last_sync=last_sync,
            **kwargs
        )

        for attendance in data:
            yield Attendance.load(attendance)
