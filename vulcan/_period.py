from related import IntegerField, DateField, immutable

from ._utils import dict_only


@immutable
class Period:
    """
    Okres kwalifikacyjny

    Attributes:
        id (:class:`int`): ID okresu kwalifikacyjnego
        number (:class:`int`): Liczba kolejna okresu kwalifikacyjnego
        level (:class:`int`): Poziom (klasa) okresu kwalifikacyjnego
        from_ (:class:`datetime.date`): Data rozpoczęcia okresu kwalifikacyjnego
        to (:class:`datetime.date`): Data zakończenia okresu kwalifikacyjnego
    """

    id = IntegerField(key="IdOkresKlasyfikacyjny")
    number = IntegerField(key="OkresNumer")
    level = IntegerField(key="OkresPoziom")
    from_ = DateField(key="OkresDataOdTekst", required=False)
    to = DateField(key="OkresDataDoTekst", required=False)

    @staticmethod
    def only_keys(json):
        return dict_only(
            json,
            {
                "IdOkresKlasyfikacyjny",
                "OkresNumer",
                "OkresPoziom",
                "OkresDataOdTekst",
                "OkresDataDoTekst",
            },
        )
