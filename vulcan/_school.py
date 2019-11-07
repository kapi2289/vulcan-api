from related import IntegerField, StringField, immutable

from ._utils import dict_only


@immutable
class School:
    """
    Szkoła

    Attributes:
        id (:class:`int`) ID szkoły
        name (:class:`str`) Pełna nazwa szkoły
        short (:class:`str`) Skrót nazwy szkoły
        symbol (:class:`str`) Symbol szkoły
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
