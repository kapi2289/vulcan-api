from datetime import datetime

from related import (
    IntegerField,
    immutable,
    TimeField,
    StringField,
    DateField,
    ChildField,
)

from ._subject import Subject
from ._teacher import Teacher
from ._utils import TIME_FORMAT_H_M


@immutable
class LessonTime:
    """
    Pora lekcji

    Attributes:
        id (:class:`int`): ID pory lekcji
        number (:class:`int`): Numer kolejny pory lekcji
        from_ (:class:`datetime.time`): Godzina i minuta rozpoczęcia lekcji
        to (:class:`datetime.time`): Godzina i minuta zakończenia lekcji
    """

    id = IntegerField(key="Id")
    number = IntegerField(key="Numer")
    from_ = TimeField(key="PoczatekTekst", formatter=TIME_FORMAT_H_M)
    to = TimeField(key="KoniecTekst", formatter=TIME_FORMAT_H_M)


@immutable
class Lesson:
    """
    Lekcja

    Attributes:
        number (:class:`int`): Numer lekcji
        room (:class:`string`): Sala, w której odbywa się lekcja
        group (:class:`string`): Grupa która odbywa lekcję
        date (:class:`datetime.date`): Data lekcji
        from_ (:class:`datetime.datetime`): Data i godzina rozpoczęcia lekcji
        to (:class:`datetime.datetime`): Data i godzina zakończenia lekcji
        time (:class:`vulcan.LessonTime`): Informacje o porze lekcji
        teacher (:class:`vulcan.Teacher`): Nauczyciel prowadzący lekcję
        subject (:class:`vulcan.Subject`): Przedmiot na lekcji
    """

    number = IntegerField(key="NumerLekcji")
    room = StringField(key="Sala", required=False)
    group = StringField(key="PodzialSkrot", required=False)
    date = DateField(key="DzienTekst", required=False)

    time = ChildField(LessonTime, required=False)
    teacher = ChildField(Teacher, required=False)
    subject = ChildField(Subject, required=False)

    @property
    def from_(self):
        return datetime.combine(self.date, self.time.from_)

    @property
    def to(self):
        return datetime.combine(self.date, self.time.to)
