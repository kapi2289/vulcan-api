from related import (
    immutable,
    IntegerField,
    StringField,
    FloatField,
    DateTimeField,
    ChildField,
)

from ._subject import Subject
from ._teacher import Teacher


@immutable
class GradeCategory:
    """
    Kategoria oceny

    Attributes:
        id (:class:`id`): Id kategorii
        name (:class:`str`): Pełna nazwa kategorii
        short (:class:`str`): Kod (skrót) nazwy kategorii
    """

    id = IntegerField(key="Id")
    name = StringField(key="Nazwa")
    short = StringField(key="Kod")


@immutable
class Grade:
    """
    Ocena cząstkowa

    Attributes:
        id (:class:`int`): ID oceny
        content (:class:`str`): Wpis oceny
        value (:class:`float`): Wartość oceny (przydaytna do obliczania średniej)
        weight (:class:`float`): Waga oceny
        description (:class:`str`): Opis oceny
        date (:class:`datetime.datetime`): Data wpisania oceny
        last_modification_date (:class:`datetime.datetime`): Data ostatniej modyfikacji oceny
        teacher (:class:`vulcan.models.Teacher`): Nauczyciel, który wpisał ocenę
        subject (:class:`vulcan.models.Subject`): Przedmiot, z którego dostano ocenę
        category (:class:`vulcan.models.GradeCategory`): Kategoria oceny
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
