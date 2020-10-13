# -*- coding: utf-8 -*-

from related import immutable, StringField, IntegerField

from ._serializable import Serializable


@immutable
class Teacher(Serializable):
    """A teacher or other school employee.

    :var int ~.id: teacher ID
    :var str ~.name: teacher's name
    :var str ~.surname: teacher's surname
    :var str ~.display_name: teacher's display name
    """

    id = IntegerField(key="Id")
    name = StringField(key="Name")
    surname = StringField(key="Surname")
    display_name = StringField(key="DisplayName")
