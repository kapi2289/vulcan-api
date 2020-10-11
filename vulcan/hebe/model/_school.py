# -*- coding: utf-8 -*-

from related import immutable, StringField, IntegerField

from ._serializable import Serializable


@immutable
class School(Serializable):
    """A single school building.

    :var int ~.id: school ID
    :var str ~.name: school full name
    :var str ~.short_name: school short name
    :var str ~.address: school address (location)
    """

    id = IntegerField(key="Id")
    name = StringField(key="Name")
    short_name = StringField(key="Short")
    address = StringField(key="Address")
