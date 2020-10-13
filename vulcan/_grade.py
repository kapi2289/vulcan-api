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

    :var id ~.id: Category ID
    :var str ~.name: Full category name
    :var str ~.short: Short name of the category
    """

    id = IntegerField(key="Id")
    name = StringField(key="Nazwa")
    short = StringField(key="Kod")


@immutable
class Grade:
    """Grade

    :var int ~.id: Grade ID
    :var str ~.content: Grade content
    :var float ~.weight: Grade weight
    :var str ~.description: Grade description
    :var `datetime.datetime` ~.date: Grade creation date
    :var `datetime.datetime` ~.last_modification_date: Last grade modification date
    :var float ~.value: Grade value (you can use it to calculate the average)
    :var `~vulcan._teacher.Teacher` ~.teacher: Teacher, who added the grade
    :var `~vulcan._subject.Subject` ~.subject: Subject, from which student received the grade
    :var `~vulcan._grade.GradeCategory` ~.category: Grade category
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
