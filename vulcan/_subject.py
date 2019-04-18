class Przedmiot:
    """
    Przedmiot

    Attributes:
        id (:class:`int`): ID przedmiotu
        nazwa (:class:`str`): Pełna nazwa przedmiotu
        kod (:class:`str`): Kod nazwy przedmiotu
    """

    def __init__(self, id=None, nazwa=None, kod=None):
        self.id = id
        self.nazwa = nazwa
        self.kod = kod

    def __repr__(self):
        return "<Przedmiot {!r}>".format(self.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        nazwa = j.get("Nazwa")
        kod = j.get("Kod")
        return cls(id=id, nazwa=nazwa, kod=kod)
