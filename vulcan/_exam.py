from aenum import Enum, unique
from related import immutable, IntegerField, StringField, ChildField, DateField

from ._subject import Subject
from ._teacher import Teacher


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
