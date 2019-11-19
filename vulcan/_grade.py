# -*- coding: utf-8 -*-

from related import (
    immutable,
    IntegerField,
    StringField,
    FloatField,
    DateTimeField,
    ChildField,
    to_model,
)

from ._subject import Subject
from ._teacher import Teacher


@immutable
class GradeCategory:
    """
    Grade category

    Attributes:
        id (:class:`id`): Category ID
        name (:class:`str`): Full category name
        short (:class:`str`): Short name of the category
    """

    id = IntegerField(key="Id")
    name = StringField(key="Nazwa")
    short = StringField(key="Kod")


@immutable
class Grade:
    """
    Grade

    Attributes:
        id (:class:`int`): Grade ID
        content (:class:`str`): Grade content
        value (:class:`float`): Grade value (you can use it to calculate the average)
        weight (:class:`float`): Grade weight
        description (:class:`str`): Grade description
        date (:class:`datetime.datetime`): Grade creation date
        last_modification_date (:class:`datetime.datetime`): Last grade modification date
        teacher (:class:`vulcan._teacher.Teacher`): Teacher, who added the grade
        subject (:class:`vulcan._subject.Subject`): Subject, from which student received the grade
        category (:class:`vulcan._grade.GradeCategory`): Grade category
    """

    id = IntegerField(key="Id")
    content = StringField(key="Wpis")
    value = FloatField(key="Wartosc")
    weight = FloatField(key="WagaOceny")
    description = StringField(key="Opis")
    date = DateTimeField(key="DataUtworzeniaTekst")
    last_modification_date = DateTimeField(key="DataModyfikacjiTekst")

    teacher = ChildField(Teacher, required=False)
    subject = ChildField(Subject, required=False)
    category = ChildField(GradeCategory, required=False)

    @classmethod
    def get(cls, api):
        j = api.post("Uczen/Oceny")

        for grade in j.get("Data", []):
            grade["teacher"] = api.dict.get_teacher(grade["IdPracownikD"])
            grade["subject"] = api.dict.get_subject(grade["IdPrzedmiot"])
            grade["category"] = api.dict.get_category(grade["IdKategoria"])

            yield to_model(cls, grade)
