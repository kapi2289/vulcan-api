# -*- coding: utf-8 -*-

import datetime

from related import (
    IntegerField,
    immutable,
    TimeField,
    StringField,
    BooleanField,
    DateField,
    ChildField,
    to_model,
)

from ._subject import Subject
from ._teacher import Teacher
from ._utils import TIME_FORMAT_H_M, sort_and_filter_dates


@immutable
class LessonTime:
    """Lesson time (start-end range)

    :var int ~.id: Lesson time ID
    :var int ~.number: Lesson number
    :var `datetime.time` ~.from_: Lesson start time
    :var `datetime.time` ~.to: Lesson end time
    """

    id = IntegerField(key="Id")
    number = IntegerField(key="Numer")
    from_ = TimeField(key="PoczatekTekst", formatter=TIME_FORMAT_H_M)
    to = TimeField(key="KoniecTekst", formatter=TIME_FORMAT_H_M)


@immutable
class Lesson:
    """Lesson

    :var int ~.number: Lesson number
    :var str ~.room: Classroom, in which is the lesson
    :var str ~.group: Group, that has the lesson
    :var `datetime.date` ~.date: Lesson date
    :var str ~.changes: Lesson changes
    :var bool ~.visible: Lesson visibility (whether the timetable applies to the given student)
    :var `datetime.datetime` ~.from_: Lesson start date and time
    :var `datetime.datetime` ~.to: Lesson end date and time
    :var `~vulcan._lesson.LessonTime` ~.time: Information about the lesson time
    :var `~vulcan._teacher.Teacher` ~.teacher: Teacher of the lesson
    :var `~vulcan._subject.Subject` ~.subject: Subject on the lesson
    """

    number = IntegerField(key="NumerLekcji")
    room = StringField(key="Sala", required=False)
    group = StringField(key="PodzialSkrot", required=False)
    date = DateField(key="DzienTekst", required=False)
    changes = StringField(key="AdnotacjaOZmianie", required=False)
    visible = BooleanField(key="PlanUcznia", required=False)

    time = ChildField(LessonTime, required=False)
    teacher = ChildField(Teacher, required=False)
    subject = ChildField(Subject, required=False)

    # pylint: disable=E1101
    @property
    def from_(self):
        return datetime.datetime.combine(self.date, self.time.from_)

    # pylint: disable=E1101
    @property
    def to(self):
        return datetime.datetime.combine(self.date, self.time.to)

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

        j = api.post("Uczen/PlanLekcjiZeZmianami", json=data)

        lessons = sort_and_filter_dates(
            j.get("Data", []),
            date_from,
            date_to,
            sort_key="NumerLekcji",
            date_key="DzienTekst",
        )

        for lesson in lessons:
            lesson["time"] = api.dict.get_lesson_time_json(lesson["IdPoraLekcji"])
            lesson["teacher"] = api.dict.get_teacher_json(lesson["IdPracownik"])
            lesson["subject"] = api.dict.get_subject_json(lesson["IdPrzedmiot"])

            yield to_model(cls, lesson)
