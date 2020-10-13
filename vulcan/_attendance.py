# -*- coding: utf-8 -*-

import datetime

from related import (
    IntegerField,
    StringField,
    DateField,
    BooleanField,
    ChildField,
    immutable,
    to_model,
)

from ._lesson import LessonTime
from ._utils import sort_and_filter_dates


@immutable
class AttendanceCategory:
    """Attendance Category

    :var int ~.id: Attendance ID
    :var str ~.name: Attendance name
    :var bool ~.presence: Presence on lesson
    :var bool ~.absence: Absence on lesson
    :var bool ~.exemption: Exemption from lesson
    :var bool ~.late: Is late for lesson
    :var bool ~.justified: Justified absence
    :var bool ~.deleted: Whether the entry is deleted
    """

    id = IntegerField(key="Id")
    name = StringField(key="Nazwa")
    presence = BooleanField(key="Obecnosc")
    absence = BooleanField(key="Nieobecnosc")
    exemption = BooleanField(key="Zwolnienie")
    late = BooleanField(key="Spoznienie")
    justified = BooleanField(key="Usprawiedliwione")
    deleted = BooleanField(key="Usuniete")


@immutable
class Attendance:
    """Attendance

    :var `~vulcan._subject.Subject` ~.subject: Subject of the lesson
    :var `datetime.date` ~.date: Attendance date
    :var `~vulcan._lesson.LessonTime` ~.time: Information about the lesson time
    :var `~vulcan._attendance.AttendanceCategory` ~.category: Information about Attendance category
    """

    subject = StringField(key="PrzedmiotNazwa")
    date = DateField(key="DzienTekst")

    time = ChildField(LessonTime, required=False)
    category = ChildField(AttendanceCategory, required=False)

    @classmethod
    def get(cls, api, date_from, date_to):
        if not date_from:
            date_from = datetime.date.today()
        if not date_to:
            date_to = date_from

        data = {
            "DataPoczatkowa": date_from.strftime("%Y-%m-%d"),
            "DataKoncowa": date_to.strftime("%Y-%m-%d"),
        }

        j = api.post("Uczen/Frekwencje", json=data)

        attendances = sort_and_filter_dates(
            j.get("Data", {}).get("Frekwencje", []),
            date_from,
            date_to,
            sort_key="Numer",
            date_key="DzienTekst",
        )

        for attendance in attendances:
            attendance["time"] = api.dict.get_lesson_time_json(
                attendance["IdPoraLekcji"]
            )
            attendance["category"] = api.dict.get_attendance_category_json(
                attendance["IdKategoria"]
            )

            yield to_model(cls, attendance)
