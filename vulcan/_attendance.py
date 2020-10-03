# -*- coding: utf-8 -*-

import datetime

from related import (
    IntegerField,
    StringField,
    DateField,
    BooleanField,
    ChildField,
    TimeField,
    immutable,
    to_model,
)

from ._utils import TIME_FORMAT_H_M, sort_and_filter_dates
from ._lesson import LessonTime


@immutable
class AttendanceCategory:
    """
    Attendance Category

    Attributes:
        id (:class:`int`): Lesson timeAttendance ID
        name (:class:`string`): Attendance name
        presence (:class:`boolean`): Presence on lesson
        absence (:class:`boolean`): Absence on lesson
        exemption (:class:`boolean`): Exemption from lesson
        late (:class:`boolean`): Be late for lesson
        justified (:class:`boolean`): Justified lesson
        deleted (:class:`boolean`): Whether the entry is deleted
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
    """
    Attendance

    Attributes:
        subject (:class:`vulcan._subject.Subject`): Subject on the lesson
        date (:class:`datetime.date`): Attendance date
        time (:class:`vulcan._lesson.LessonTime`): Information about the lesson time
        category (:class:`vulcan._attendance.AttendanceCategory`): Information about Attendance category

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
