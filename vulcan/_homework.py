from related import IntegerField, StringField, DateField, ChildField, immutable

from ._subject import Subject
from ._teacher import Teacher


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
