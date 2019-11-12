# -*- coding: utf-8 -*-

from datetime import datetime

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
from ._utils import sort_and_filter_date


@immutable
class Homework:
    """
    Zadanie domowe

    Attributes:
        id (:class:`int`): ID zadania domowego
        description (:class:`str`): Opis zadania domowego
        date (:class:`datetime.date`): Data zadania domowego
        teacher (:class:`vulcan.models.Teacher`): Nauczyciel, który wpisał to zadanie
        subject (:class:`vulcan.models.Subject`): Przedmiot, z którego jest zadane zadanie
    """

    id = IntegerField(key="Id")
    description = StringField(key="Opis")
    date = DateField(key="DataTekst")

    teacher = ChildField(Teacher, required=False)
    subject = ChildField(Subject, required=False)

    @classmethod
    def get(cls, api, date=None):
        if not date:
            date = datetime.now()
        date_str = date.strftime("%Y-%m-%d")

        data = {"DataPoczatkowa": date_str, "DataKoncowa": date_str}

        j = api.post("Uczen/ZadaniaDomowe", json=data)

        homework_list = sort_and_filter_date(j.get("Data", []), date_str)

        for homework in homework_list:
            homework["teacher"] = api.dict.get_teacher(homework["IdPracownik"])
            homework["subject"] = api.dict.get_subject(homework["IdPrzedmiot"])

            yield to_model(cls, homework)
