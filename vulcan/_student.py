# -*- coding: utf-8 -*-

from aenum import Enum, unique
from related import IntegerField, immutable, StringField, ChildField, to_model

from ._class import Class
from ._period import Period
from ._school import School


@unique
class Gender(Enum):
    """Płeć"""

    WOMAN = 0
    MAN = 1


@immutable
class Student:
    """
    Uczeń

    Attributes:
        id (:class:`int`): ID ucznia
        login_id (:class:`int`) ID zalogowanego konta rodzica lub ucznia
        first_name (:class:`str`): Pierwsze imię ucznia
        second_name (:class:`str` or :class:`None`): Drugie imię ucznia
        last_name (:class:`str`): Nazwisko ucznia
        name (:class:`str`): Imię, drugie imię oraz nazwisko ucznia
        gender (:class:`vulcan.Gender`): Płeć ucznia
        nick (:class:`str`): Pseudonim ucznia
        period (:class:`vulcan.Period`): Aktualny okres klasyfikacyjny ucznia
        class_ (:class:`vulcan.Class`): Klasa ucznia
        school (:class:`vulcan.School`): Szkoła ucznia
    """

    id = IntegerField(key="Id")
    login_id = IntegerField(key="UzytkownikLoginId")
    first_name = StringField(key="Imie")
    second_name = StringField(key="Imie2")
    last_name = StringField(key="Nazwisko")
    gender = ChildField(Gender, key="UczenPlec")
    nick = StringField(key="Pseudonim", required=False)

    period = ChildField(Period, required=False)
    class_ = ChildField(Class, required=False)
    school = ChildField(School, required=False)

    @property
    def name(self):
        first = "{} {}".format(self.first_name, self.second_name).rstrip()
        return "{} {}".format(first, self.last_name)

    @staticmethod
    def format_json(json):
        json["period"] = Period.only_keys(json)
        json["class_"] = Class.only_keys(json)
        json["school"] = School.only_keys(json)
        return json

    @classmethod
    def get(cls, api):
        j = api.post(api.base_url + "UczenStart/ListaUczniow")

        for student in j.get("Data", []):
            yield to_model(cls, cls.format_json(student))
