# -*- coding: utf-8 -*-

from related import IntegerField, StringField, immutable

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

    id: int = IntegerField(key="Id")
    key: str = StringField(key="Key")
    name: str = StringField(key="Name")
    code: str = StringField(key="Kod")
    position: int = IntegerField(key="Position")
