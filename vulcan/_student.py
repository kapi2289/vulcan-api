# -*- coding: utf-8 -*-

from aenum import Enum, unique
from related import IntegerField, immutable, StringField, ChildField, to_model

from ._class import Class
from ._period import Period
from ._school import School


@unique
class Gender(Enum):
    """
    Student gender
    """

    WOMAN = 0
    MAN = 1


@immutable
class Student:
    """Student

    :var int ~.id: Student ID
    :var int ~.login_id: ID of the logged user
    :var str ~.account_name: Student account name
    :var str ~.first_name: Student first name
    :var str ~.second_name: Student second name, optional
    :var str ~.last_name: Student last name (surname)
    :var `~vulcan._student.Gender` ~.gender: Student gender
    :var str ~.nickname: Student nickname
    :var `~vulcan._period.Period` ~.period: Current student class period
    :var `~vulcan._class.Class` ~.class_: Student class
    :var `~vulcan._school.School` ~.school: Student school
    """

    id = IntegerField(key="Id")
    login_id = IntegerField(key="UzytkownikLoginId")
    account_name = StringField(key="UzytkownikNazwa")
    first_name = StringField(key="Imie")
    last_name = StringField(key="Nazwisko")
    gender = ChildField(Gender, key="UczenPlec")
    second_name = StringField(key="Imie2", required=False)
    nickname = StringField(key="Pseudonim", required=False)

    period = ChildField(Period, required=False)
    class_ = ChildField(Class, required=False)
    school = ChildField(School, required=False)

    @property
    def name(self):
        """Returns the student's full name as "Name SecondName Surname".

        :rtype: str
        """
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
