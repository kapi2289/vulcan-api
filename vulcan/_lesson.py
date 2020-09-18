# -*- coding: utf-8 -*-

import datetime

from related import (
    IntegerField,
    immutable,
    TimeField,
    StringField,
    DateField,
    ChildField,
    to_model,
)

from ._subject import Subject
from ._teacher import Teacher
from ._utils import TIME_FORMAT_H_M, sort_and_filter_dates


@immutable
class LessonTime:
    """
    Lesson time

    Attributes:
        id (:class:`int`): Lesson time ID
        number (:class:`int`): Lesson number
        from_ (:class:`datetime.time`): Lesson start time
        to (:class:`datetime.time`): Lesson end time
    """

    id = IntegerField(key="Id")
    number = IntegerField(key="Numer")
    from_ = TimeField(key="PoczatekTekst", formatter=TIME_FORMAT_H_M)
    to = TimeField(key="KoniecTekst", formatter=TIME_FORMAT_H_M)


@immutable
class Lesson:
    """
    Lesson

    Attributes:
        number (:class:`int`): Lesson number
        room (:class:`string`): Classroom, in which is the lesson
        group (:class:`string`): Group, that has the lesson
        date (:class:`datetime.date`): Lesson date
        changes (:class:`string`): Lesson changes
        from_ (:class:`datetime.datetime`): Lesson start date and time
        to (:class:`datetime.datetime`): Lesson end date and time
        time (:class:`vulcan._lesson.LessonTime`): Information about the lesson time
        teacher (:class:`vulcan._teacher.Teacher`): Teacher of the lesson
        subject (:class:`vulcan._subject.Subject`): Subject on the lesson
    """

    number = IntegerField(key="NumerLekcji")
    room = StringField(key="Sala", required=False)
    group = StringField(key="PodzialSkrot", required=False)
    date = DateField(key="DzienTekst", required=False)
    changes = StringField(key="AdnotacjaOZmianie", required=False)

    time = ChildField(LessonTime, required=False)
    teacher = ChildField(Teacher, required=False)
    subject = ChildField(Subject, required=False)

    @property
    def from_(self):
        return datetime.datetime.combine(self.date, self.time.from_)

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
