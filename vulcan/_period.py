# -*- coding: utf-8 -*-

from related import IntegerField, DateField, immutable

from ._utils import dict_only


@immutable
class Period:
    """School year period

    :var int ~.id: Period ID
    :var int ~.number: Number of the period
    :var int ~.level: Level (class level) of the period
    :var `datetime.date` ~.from_: Period start date
    :var `datetime.date` ~.to: Period end date
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
