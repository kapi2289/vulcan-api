# -*- coding: utf-8 -*-

from related import IntegerField, StringField, immutable


@immutable
class Subject:
    """School subject

    :param int id: Subject ID
    :param str name: Subject full name
    :param str short: Short name of the subject
    :param int position: Position of the subject in subjects list
    """

    id = IntegerField(key="Id")
    name = StringField(key="Nazwa")
    short = StringField(key="Kod")
    position = IntegerField(key="Pozycja")
