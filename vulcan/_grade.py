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
    """Grade category

    :param id id: Category ID
    :param str name: Full category name
    :param str short: Short name of the category
    """

    id = IntegerField(key="Id")
    name = StringField(key="Nazwa")
    short = StringField(key="Kod")


@immutable
class Grade:
    """Grade

    :param int id: Grade ID
    :param str content: Grade content
    :param float weight: Grade weight
    :param str description: Grade description
    :param `datetime.datetime` date: Grade creation date
    :param `datetime.datetime` last_modification_date: Last grade modification date
    :param float value: Grade value (you can use it to calculate the average)
    :param `vulcan._teacher.Teacher` teacher: Teacher, who added the grade
    :param `vulcan._subject.Subject` subject: Subject, from which student received the grade
    :param `vulcan._grade.GradeCategory` category: Grade category
    """

    id = IntegerField(key="Id")
    content = StringField(key="Wpis")
    weight = FloatField(key="WagaOceny")
    description = StringField(key="Opis")
    date = DateTimeField(key="DataUtworzeniaTekst")
    last_modification_date = DateTimeField(key="DataModyfikacjiTekst")
    value = FloatField(key="Wartosc", required=False)

    teacher = ChildField(Teacher, required=False)
    subject = ChildField(Subject, required=False)
    category = ChildField(GradeCategory, required=False)

    @classmethod
    def get(cls, api):
        j = api.post("Uczen/Oceny")

        for grade in j.get("Data", []):
            grade["teacher"] = api.dict.get_teacher_json(grade["IdPracownikD"])
            grade["subject"] = api.dict.get_subject_json(grade["IdPrzedmiot"])
            grade["category"] = api.dict.get_grade_category_json(grade["IdKategoria"])

            yield to_model(cls, grade)
