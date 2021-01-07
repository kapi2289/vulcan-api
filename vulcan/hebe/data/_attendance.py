# -*- coding: utf-8 -*-
from typing import AsyncIterator, Union, List
import datetime

from related import (
    immutable,
    IntegerField,
    StringField,
    FloatField,
    ChildField,
    BooleanField,
)

from .._api_helper import FilterType
from .._endpoints import DATA_ATTENDANCE
from ..model import (
    Serializable,
    DateTime,
    Teacher,
    Subject,
    Period,
    TimeSlot,
    TeamClass,
    TeamVirtual,
)


@immutable
class PresenceType(Serializable):
    """Presence type

    :var int ~.id: Attendance ID
    :var str ~.name: Attendance name
    :var str ~.symbol: Attendance symbol
    :var int ~.category_id: Attendance category ID
    :var str ~.category_name: Attendance category name
    :var int ~.position: Attendance position
    :var bool ~.presence: Presence on lesson
    :var bool ~.absence: Absence on lesson
    :var bool ~.exemption: Exemption from lesson
    :var bool ~.late: Is late for lesson
    :var bool ~.justified: Justified absence
    :var bool ~.deleted: Whether the entry is deleted
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
    """A grade.

    :var int ~.lesson_id: Lesson ID
    :var int ~.id: Attendance ID
    :var int ~.lesson_number: Lesson number
    :var str ~.global_key: Attendance global key
    :var int ~.lesson_class_id: Lesson class ID
    :var str ~.global_key: Lesson class global key
    :var bool ~.calculate_presence: Does it count for absences
    :var bool ~.replacement: Is it replaced
    :var `~vulcan.hebe.model.Subject` ~.subject: Subject of the lesson
    :var str ~.topic: Topic of the lesson
    :var `~vulcan.hebe.model.Teacher` ~.teacher: Teacher of the lesson
    :var `~vulcan.hebe.model.Teacher` ~.second_teacher: Seccond teacher of the lesson
    :var `~vulcan.hebe.model.Teacher` ~.main_teacher: Pupil main teacher
    :var `~vulcan.hebe.model.TeamClass` ~.team_class: The class that had lesson
    :var str ~.class_alias: Class short name
    :var `~vulcan.hebe.model.DateTime` ~.date: lesson's date
    :var `~vulcan.hebe.model.TimeSlot` ~.time: lesson's time
    :var `~vulcan.hebe.model.DateTime` ~.date_modified: Attendance modification date, if not modified it is created date
    :var int ~.id: Aux presence ID
    :var str ~.justification_status: Attendance justification status
    :var `~vulcan.hebe.data.PresenceType` ~.presence_type: PresenceType
    :var str ~.note: Attendance note
    :var str ~.public_resources: Attendance public esources
    :var str ~.remote_resources: Attendance remote resources
    :var `~vulcan.hebe.model.TeamVirtual` ~.group: Group, that has the lesson
    :var bool ~.visible: Attendance visibility


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
        if date_from == None:
            date_from = datetime.date.today()
        if date_to == None:
            date_to = date_from
        date_to = date_to + datetime.timedelta(
            days=1
        )  # Vulcan requires the date_to to be one greater the date it is supposed to be
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.hebe.data.Attendance`], List[int]]
        """
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
