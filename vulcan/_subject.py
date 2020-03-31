# -*- coding: utf-8 -*-

from related import IntegerField, StringField, immutable


@immutable
class Subject:
    """
    School subject

    Attributes:
        id (:class:`int`): Subject ID
        name (:class:`str`): Subject full name
        short (:class:`str`): Short name of the subject
        position (:class:`int`) Position of the subject in subjects list
    """

    id = IntegerField(key="Id")
    name = StringField(key="Nazwa")
    short = StringField(key="Kod")
    position = IntegerField(key="Pozycja")
