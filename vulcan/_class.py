# -*- coding: utf-8 -*-

from related import immutable, IntegerField, StringField

from ._utils import dict_only


@immutable
class Class:
    """Class

    :var int ~.id: Class ID
    :var int ~.level: Class level (eg. `8`)
    :var str ~.name: Class name (eg. `"8A"`)
    :var str ~.symbol: Class symbol (eg. `"A"`)
    """

    id = IntegerField(key="IdOddzial")
    level = IntegerField(key="OkresPoziom")
    name = StringField(key="OddzialKod", required=False)
    symbol = StringField(key="OddzialSymbol", required=False)

    @staticmethod
    def only_keys(json):
        return dict_only(
            json, {"IdOddzial", "OddzialKod", "OkresPoziom", "OddzialSymbol"}
        )
