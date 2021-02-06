# -*- coding: utf-8 -*-

from related import IntegerField, StringField, immutable

from ._serializable import Serializable


@immutable
class TeamClass(Serializable):
    """A school class.

    :var int ~.id: class ID
    :var str ~.key: class's key (UUID)
    :var str ~.display_name: class's display name
    :var str ~.symbol: class's symbol (e.g. a letter after the level, "C" in "6C")
    """

    id: int = IntegerField(key="Id")
    key: str = StringField(key="Key")
    display_name: str = StringField(key="DisplayName")
    symbol: str = StringField(key="Symbol")


@immutable
class TeamVirtual(Serializable):
    """A virtual team, i.e. a part of the school class. Often called
    a "distribution" of the class.

    :var int ~.id: team ID
    :var str ~.key: team's key (UUID)
    :var str ~.shortcut: team's short name
    :var str ~.name: team's name
    :var str ~.part_type: type of the distribution
    """

    id: int = IntegerField(key="Id")
    key: str = StringField(key="Key")
    shortcut: str = StringField(key="Shortcut")
    name: str = StringField(key="Name")
    part_type: str = StringField(key="PartType")
