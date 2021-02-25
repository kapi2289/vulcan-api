# -*- coding: utf-8 -*-

from related import StringField, immutable

from ._serializable import Serializable


@immutable
class Attachment(Serializable):
    """An attachment

    :var str ~.name: Name
    :var str ~.link: Link
    """

    name: str = StringField(key="Name")
    link: str = StringField(key="Link")
