# -*- coding: utf-8 -*-

from aenum import Enum, unique
from related import IntegerField, immutable, StringField, ChildField, to_model

from ._class import Class
from ._period import Period
from ._school import School


@unique
class Gender(Enum):
    """Studen gender"""

    WOMAN = 0
    MAN = 1


@immutable
class Student:
    """
    Student

    Attributes:
        id (:class:`int`): Student ID
        login_id (:class:`int`) ID of the logged user
        first_name (:class:`str`): Student first name
        second_name (:class:`str` or :class:`None`): Student second name
        last_name (:class:`str`): Student last name (surname)
        name (:class:`str`): Student full name
        gender (:class:`vulcan._student.Gender`): Student gender
        nickname (:class:`str`): Student nickname
        period (:class:`vulcan._period.Period`): Current student class period
        class_ (:class:`vulcan._class.Class`): Student class
        school (:class:`vulcan._school.School`): Student school
    """

    id = IntegerField(key="Id")
    login_id = IntegerField(key="UzytkownikLoginId")
    first_name = StringField(key="Imie")
    second_name = StringField(key="Imie2")
    last_name = StringField(key="Nazwisko")
    gender = ChildField(Gender, key="UczenPlec")
    nickname = StringField(key="Pseudonim", required=False)

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
