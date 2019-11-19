# -*- coding: utf-8 -*-

from related import IntegerField, StringField, immutable

from ._utils import dict_only


@immutable
class School:
    """
    School

    Attributes:
        id (:class:`int`) School ID
        name (:class:`str`) School full name
        short (:class:`str`) Short name of the school
        symbol (:class:`str`) School symbol
    """

    id = IntegerField(key="IdJednostkaSprawozdawcza")
    name = StringField(key="JednostkaSprawozdawczaNazwa")
    short = StringField(key="JednostkaSprawozdawczaSkrot")
    symbol = StringField(key="JednostkaSprawozdawczaSymbol")

    @staticmethod
    def only_keys(json):
        return dict_only(
            json,
            {
                "IdJednostkaSprawozdawcza",
                "JednostkaSprawozdawczaNazwa",
                "JednostkaSprawozdawczaSkrot",
                "JednostkaSprawozdawczaSymbol",
            },
        )
