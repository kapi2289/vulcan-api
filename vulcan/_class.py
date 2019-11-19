# -*- coding: utf-8 -*-

from related import immutable, IntegerField, StringField

from ._utils import dict_only


@immutable
class Class:
    """
    Attributes:
        id (:class:`int`): Class ID
        level (:class:`int`): Class level (eg. `8`)
        name (:class:`str`): Class name (eg. `"8A"`)
        symbol (:class:`str`): Class symbol (eg. `"A"`)
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
