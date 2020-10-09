# -*- coding: utf-8 -*-

from related import immutable, IntegerField, StringField


@immutable
class Teacher:
    """
    School teacher or employee

    Attributes:
        id (:class:`int`): Teacher ID
        first_name (:class:`str`): Teacher first name
        last_name (:class:`str`): Teacher last name (surname)
        name (:class:`str`): Teacher full name
        short (:class:`str`): Code (short name) of the teacher
        login_id (:class:`int`): Teacher account ID
    """

    id = IntegerField(key="Id")
    first_name = StringField(key="Imie")
    last_name = StringField(key="Nazwisko")
    short = StringField(key="Kod")
    login_id = IntegerField(key="LoginId")

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def name_reversed(self):
        return "{} {}".format(self.last_name, self.first_name)
