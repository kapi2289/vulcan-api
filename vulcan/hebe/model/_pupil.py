# -*- coding: utf-8 -*-

from aenum import Enum, unique
from related import immutable, StringField, IntegerField, ChildField

from ._serializable import Serializable


@unique
class Gender(Enum):
    """Student gender"""

    WOMAN = False
    MAN = True


@immutable
class Pupil(Serializable):
    """A class containing the student's data.

    :var int ~.id: pupil's ID
    :var int ~.login_id: pupil's account login ID
    :var str ~.login_value: pupil's account login name (email/username)
    :var str ~.first_name: student's first name
    :var str ~.second_name: student's second name, optional
    :var str ~.last_name: student's last name / surname
    :var `~vulcan.hebe.model.Gender` ~.gender: student's gender
    """

    id = IntegerField(key="Id")
    login_id = IntegerField(key="LoginId")
    login_value = StringField(key="LoginValue")
    first_name = StringField(key="FirstName")
    second_name = StringField(key="SecondName")
    last_name = StringField(key="Surname")
    gender = ChildField(Gender, key="Sex")
