# -*- coding: utf-8 -*-

from related import immutable, IntegerField, StringField

from ._utils import dict_only


@immutable
class Class:
    """Class

    :param int id: Class ID
    :param int level: Class level (eg. `8`)
    :param str name: Class name (eg. `"8A"`)
    :param str symbol: Class symbol (eg. `"A"`)
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
