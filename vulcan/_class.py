# -*- coding: utf-8 -*-

from related import immutable, IntegerField, StringField

from ._utils import dict_only


@immutable
class Class:
    """
    Oddział (klasa)

    Attributes:
        id (:class:`int`): ID klasy
        level (:class:`int`): Poziom klasy (np. `8`)
        name (:class:`str`): Nazwa klasy (np. `"8A"`)
        symbol (:class:`str`): Symbol klasy (np. `"A"`)
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
