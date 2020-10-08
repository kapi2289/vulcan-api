# -*- coding: utf-8 -*-

from related import immutable, StringField, IntegerField, ChildField
from ._serializable import Serializable

from aenum import Enum, unique


@unique
class Gender(Enum):
    """Student gender"""

    WOMAN = False
    MAN = True


@immutable
class Pupil(Serializable):
    id = IntegerField(key="Id")
    login_id = StringField(key="LoginId")
    login_value = StringField(key="LoginValue")
    first_name = StringField(key="FirstName")
    second_name = StringField(key="SecondName")
    last_name = StringField(key="Surname")
    gender = ChildField(Gender, key="Sex")
