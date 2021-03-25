# -*- coding: utf-8 -*-

from related import IntegerField, StringField, immutable

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

    id: int = IntegerField(key="Id")
    code: str = StringField(key="Symbol")
    name: str = StringField(key="Name")
    short_name: str = StringField(key="Short")
    display_name: str = StringField(key="DisplayName")
    rest_url: str = StringField(key="RestURL")
    address: str = StringField(key="Address", required=False)
