# -*- coding: utf-8 -*-

from related import immutable, StringField, IntegerField

from ._serializable import Serializable


@immutable
class Subject(Serializable):
    """A school subject.

    :var int ~.id: subject ID
    :var str ~.key: subject's key (UUID)
    :var str ~.name: subject's name
    :var str ~.code: subject's code (e.g. short name or abbreviation)
    :var int ~.position: unknown, yet
    """

    id = IntegerField(key="Id")
    key = StringField(key="Key")
    name = StringField(key="Name")
    code = StringField(key="Kod")
    position = IntegerField(key="Position")
