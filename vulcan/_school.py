class Szkola:
    """
    Szkoła

    Attributes:
        id (:class:`int`) ID szkoły
        skrot (:class:`str`) Skrót nazwy szkoły
        nazwa (:class:`str`) Pełna nazwa szkoły
        symbol (:class:`str`) Symbol szkoły
    """

    def __init__(self, id=None, skrot=None, nazwa=None, symbol=None):
        self.id = id
        self.skrot = skrot
        self.nazwa = nazwa
        self.symbol = symbol

    def __repr__(self):
        return "<Szkola {!r}>".format(self.skrot)

    @classmethod
    def from_json(cls, j):
        id = j.get("IdJednostkaSprawozdawcza")
        skrot = j.get("JednostkaSprawozdawczaSkrot")
        nazwa = j.get("JednostkaSprawozdawczaNazwa")
        symbol = j.get("JednostkaSprawozdawczaSymbol")
        return cls(id=id, skrot=skrot, nazwa=nazwa, symbol=symbol)
