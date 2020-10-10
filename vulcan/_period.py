# -*- coding: utf-8 -*-

from related import IntegerField, DateField, immutable

from ._utils import dict_only


@immutable
class Period:
    """School year period

    :param int id: Period ID
    :param int number: Number of the period
    :param int level: Level (class level) of the period
    :param `datetime.date` from_: Period start date
    :param `datetime.date` to: Period end date
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
