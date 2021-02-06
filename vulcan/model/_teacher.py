# -*- coding: utf-8 -*-

from related import IntegerField, StringField, immutable

from ._serializable import Serializable


@immutable
class Teacher(Serializable):
    """A teacher or other school employee.

    :var int ~.id: teacher ID
    :var str ~.name: teacher's name
    :var str ~.surname: teacher's surname
    :var str ~.display_name: teacher's display name
    """

    id: int = IntegerField(key="Id")
    name: str = StringField(key="Name")
    surname: str = StringField(key="Surname")
    display_name: str = StringField(key="DisplayName")
