# -*- coding: utf-8 -*-

from ..model import Serializable
from related import StringField, immutable


@immutable
class Attachment(Serializable):
    """An attachment

    :var str ~.name: Name
    :var str ~.link: Link
    """

    name: str = StringField(key="Name")
    link: str = StringField(key="Link")
