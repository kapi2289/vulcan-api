# -*- coding: utf-8 -*-

from related import immutable, IntegerField, StringField


@immutable
class Teacher:
    """
    Nauczyciel lub pracownik szkoły

    Attributes:
        id (:class:`int`): ID pracownika
        first_name (:class:`str`): Imię pracownika
        last_name (:class:`str`): Nazwisko pracownika
        name (:class:`str`): Imię oraz nazwisko pracownika
        short (:class:`str`): Kod (skrót) pracownika
        login_id (:class:`int`): ID konta pracownika
    """

    id = IntegerField(key="Id")
    first_name = StringField(key="Imie")
    last_name = StringField(key="Nazwisko")
    short = StringField(key="Kod")
    login_id = IntegerField(key="LoginId")

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)
