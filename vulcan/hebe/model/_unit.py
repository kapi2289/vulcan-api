# -*- coding: utf-8 -*-

from related import immutable, StringField, IntegerField
from ._serializable import Serializable


@immutable
class Unit(Serializable):
    id = IntegerField(key="Id")
    code = StringField(key="Symbol")
    name = StringField(key="Name")
    short_name = StringField(key="Short")
    display_name = StringField(key="DisplayName")
    address = StringField(key="Address")
    rest_url = StringField(key="RestURL")
