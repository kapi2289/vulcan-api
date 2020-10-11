# -*- coding: utf-8 -*-

from related import immutable, StringField, IntegerField

from ._serializable import Serializable


@immutable
class Unit(Serializable):
    """A group of one or more schools.

    :var int ~.id: unit ID
    :var str ~.code: unit code (school code) - often 6 digits
    :var str ~.name: unit full name
    :var str ~.short_name: unit short name
    :var str ~.display_name: unit display name
    :var str ~.address: unit address (location)
    :var str ~.rest_url: unit data's API base URL
    """

    id = IntegerField(key="Id")
    code = StringField(key="Symbol")
    name = StringField(key="Name")
    short_name = StringField(key="Short")
    display_name = StringField(key="DisplayName")
    address = StringField(key="Address")
    rest_url = StringField(key="RestURL")
