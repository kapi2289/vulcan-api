# -*- coding: utf-8 -*-

from datetime import datetime
from operator import itemgetter

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
from ._utils import TIME_FORMAT_H_M


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

    time = ChildField(LessonTime, required=False)
    teacher = ChildField(Teacher, required=False)
    subject = ChildField(Subject, required=False)

    @property
    def from_(self):
        return datetime.combine(self.date, self.time.from_)

    @property
    def to(self):
        return datetime.combine(self.date, self.time.to)

    @classmethod
    async def get(cls, api, date):
        if not date:
            date = datetime.now()
        date_str = date.strftime("%Y-%m-%d")

        data = {"DataPoczatkowa": date_str, "DataKoncowa": date_str}

        j = await api.post("Uczen/PlanLekcjiZeZmianami", json=data)

        lessons = sorted(j.get("Data", []), key=itemgetter("NumerLekcji"))
        lessons = list(filter(lambda x: x["DzienTekst"] == date_str, lessons))

        for lesson in lessons:
            lesson["time"] = api.dict.get_lesson_time_json(lesson["IdPoraLekcji"])
            lesson["teacher"] = api.dict.get_teacher_json(lesson["IdPracownik"])
            lesson["subject"] = api.dict.get_subject_json(lesson["IdPrzedmiot"])

            yield to_model(cls, lesson)
