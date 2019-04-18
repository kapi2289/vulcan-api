class Klasa:
    """
    Oddział (klasa)

    Attributes:
        id (:class:`int`): ID klasy
        kod (:class:`str`): Kod klasy (np. `"8A"`)
        poziom (:class:`int`): Poziom klasy (np. `8`)
        symbol (:class:`str`): Symbol klasy (np. `"A"`)
    """

    def __init__(self, id=None, kod=None, poziom=None, symbol=None):
        self.id = id
        self.kod = kod
        self.poziom = poziom
        self.symbol = symbol

    def __repr__(self):
        return "<Klasa {!s}>".format(self.kod)

    @classmethod
    def from_json(cls, j):
        id = j.get("IdOddzial")
        kod = j.get("OddzialKod")
        poziom = j.get("OkresPoziom")
        symbol = j.get("OddzialSymbol")
        return cls(id=id, kod=kod, poziom=poziom, symbol=symbol)
