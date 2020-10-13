# -*- coding: utf-8 -*-

from related import IntegerField, StringField, immutable

from ._utils import dict_only


@immutable
class School:
    """School

    :var int ~.id: School ID
    :var str ~.name: School full name
    :var str ~.short: Short name of the school
    :var str ~.symbol: School symbol
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
