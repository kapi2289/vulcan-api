# -*- coding: utf-8 -*-

from datetime import datetime

from aenum import Enum, unique
from related import (
    immutable,
    IntegerField,
    StringField,
    ChildField,
    DateField,
    to_model,
)

from ._subject import Subject
from ._teacher import Teacher
from ._utils import sort_and_filter_date


@unique
class ExamType(Enum):
    """
    Exam type

    Todo:
        Add test enum
    """

    EXAM = 1
    SHORT_TEST = 2
    CLASS_TEST = 3


@immutable
class Exam:
    """
    Exam, test, short test or class test

    Attributes:
        id (:class:`int`): Exam ID
        type (:class:`vulcan._exam.ExamType`): Exam type
        description (:class:`str`): Exam description
        date (:class:`datetime.date`): Exam date
        teacher (:class:`vulcan._teacher.Teacher`): Teacher, who added the exam
        subject (:class:`vulcan._subject.Subject`): Subject, from which is the exam
    """

    id = IntegerField(key="Id")
    type = ChildField(ExamType, key="RodzajNumer")
    description = StringField(key="Opis")
    date = DateField(key="DataTekst")

    teacher = ChildField(Teacher, required=False)
    subject = ChildField(Subject, required=False)

    @classmethod
    def get(cls, api, date):
        if not date:
            date = datetime.now()
        date_str = date.strftime("%Y-%m-%d")

        data = {"DataPoczatkowa": date_str, "DataKoncowa": date_str}

        j = api.post("Uczen/Sprawdziany", json=data)

        exams = sort_and_filter_date(j.get("Data", []), date_str)

        for exam in exams:
            exam["teacher"] = api.dict.get_teacher_json(exam["IdPracownik"])
            exam["subject"] = api.dict.get_subject_json(exam["IdPrzedmiot"])

            yield to_model(cls, exam)
