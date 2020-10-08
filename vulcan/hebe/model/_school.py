# -*- coding: utf-8 -*-

from related import immutable, StringField, IntegerField
from ._serializable import Serializable


@immutable
class School(Serializable):
    id = IntegerField(key="Id")
    name = StringField(key="Name")
    short_name = StringField(key="Short")
    address = StringField(key="Address")
