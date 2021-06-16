# -*- coding: utf-8 -*-

from related import IntegerField, StringField, immutable

from ._serializable import Serializable


@immutable
class School(Serializable):
    """A single school building.

    :var int ~.id: school ID
    :var str ~.name: school full name
    :var str ~.short_name: school short name
    :var str ~.address: school address (location)
    """

    id: int = IntegerField(key="Id")
    name: str = StringField(key="Name")
    short_name: str = StringField(key="Short")
    address: str = StringField(key="Address", required=False)
