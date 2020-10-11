# -*- coding: utf-8 -*-

from related import IntegerField, StringField, immutable


@immutable
class Subject:
    """School subject

    :var int ~.id: Subject ID
    :var str ~.name: Subject full name
    :var str ~.short: Short name of the subject
    :var int ~.position: Position of the subject in subjects list
    """

    id = IntegerField(key="Id")
    name = StringField(key="Nazwa")
    short = StringField(key="Kod")
    position = IntegerField(key="Pozycja")
