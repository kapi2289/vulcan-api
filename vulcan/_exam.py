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
    Rodzaj sprawdzianu

    Todo:
        Dodać enum testu
    """

    EXAM = 1
    SHORT_TEST = 2
    CLASS_TEST = 3


@immutable
class Exam:
    """
    Sprawdzian, test, praca klasowa lub kartkówka

    Attributes:
        id (:class:`int`): ID sprawdzianu
        type (:class:`vulcan.models.ExamType`): Rodzaj sprawdzianu
        description (:class:`str`): Opis sprawdzianu
        date (:class:`datetime.date`): Dzień sprawdzianu
        teacher (:class:`vulcan.models.Teacher`): Nauczyciel, który wpisał sprawdzian
        subject (:class:`vulcan.models.Subject`): Przedmiot, z którego jest sprawdzian
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
            exam["teacher"] = api.dict.get_teacher(exam["IdPracownik"])
            exam["subject"] = api.dict.get_subject(exam["IdPrzedmiot"])

            yield to_model(cls, exam)
