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

    :param int id: Attendance ID
    :param str name: Attendance name
    :param bool presence: Presence on lesson
    :param bool absence: Absence on lesson
    :param bool exemption: Exemption from lesson
    :param bool late: Is late for lesson
    :param bool justified: Justified absence
    :param bool deleted: Whether the entry is deleted
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

    :param `vulcan._subject.Subject` subject: Subject of the lesson
    :param `datetime.date` date: Attendance date
    :param `vulcan._lesson.LessonTime` time: Information about the lesson time
    :param `vulcan._attendance.AttendanceCategory` category: Information about Attendance category
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
