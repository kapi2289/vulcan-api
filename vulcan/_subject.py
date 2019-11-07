from related import IntegerField, StringField, immutable


@immutable
class Subject:
    """
    Przedmiot

    Attributes:
        id (:class:`int`): ID przedmiotu
        name (:class:`str`): Pełna nazwa przedmiotu
        short (:class:`str`): Skrót nazwy przedmiotu
    """

    id = IntegerField(key="Id")
    name = StringField(key="Nazwa")
    short = StringField(key="Kod")
