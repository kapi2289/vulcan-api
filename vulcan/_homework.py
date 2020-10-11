# -*- coding: utf-8 -*-

import datetime

from related import (
    IntegerField,
    StringField,
    DateField,
    ChildField,
    immutable,
    to_model,
)

from ._subject import Subject
from ._teacher import Teacher
from ._utils import sort_and_filter_dates


@immutable
class Homework:
    """Homework

    :var int ~.id: Homework ID
    :var str ~.description: Homework description
    :var `datetime.date` ~.date: Homework deadline date
    :var `~vulcan._teacher.Teacher` ~.teacher: Teacher, who added the homework
    :var `~vulcan._subject.Subject` ~.subject: Subject, from which is the homework
    """

    id = IntegerField(key="Id")
    description = StringField(key="Opis")
    date = DateField(key="DataTekst")

    teacher = ChildField(Teacher, required=False)
    subject = ChildField(Subject, required=False)

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

        j = api.post("Uczen/ZadaniaDomowe", json=data)

        homework_list = sort_and_filter_dates(j.get("Data", []), date_from, date_to)

        for homework in homework_list:
            homework["teacher"] = api.dict.get_teacher_json(homework["IdPracownik"])
            homework["subject"] = api.dict.get_subject_json(homework["IdPrzedmiot"])

            yield to_model(cls, homework)
