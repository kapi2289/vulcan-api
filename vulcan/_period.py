# -*- coding: utf-8 -*-

from related import IntegerField, DateField, immutable

from ._utils import dict_only


@immutable
class Period:
    """
    School year period

    Attributes:
        id (:class:`int`): Period ID
        number (:class:`int`): Number of the period
        level (:class:`int`): Level (class level) of the period
        from_ (:class:`datetime.date`): Period start date
        to (:class:`datetime.date`): Period end date
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
