# -*- coding: utf-8 -*-

from aenum import Enum, unique
from related import ChildField, IntegerField, StringField, immutable

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
    :var `~vulcan.model.Gender` ~.gender: student's gender
    """

    id: int = IntegerField(key="Id")
    login_id: int = IntegerField(key="LoginId")
    first_name: str = StringField(key="FirstName")
    last_name: str = StringField(key="Surname")
    gender: Gender = ChildField(Gender, key="Sex")
    second_name: str = StringField(key="SecondName", required=False)
    login_value: str = StringField(key="LoginValue", required=False)
