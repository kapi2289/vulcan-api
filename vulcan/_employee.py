class Pracownik:
    """
    Pracownik szkoły

    Attributes:
        id (:class:`int`): ID pracownika
        nazwa (:class:`nazwa`): Nazwisko oraz imię pracownika
        imie (:class:`str`): Imię pracownika
        nazwisko (:class:`str`): Nazwisko pracownika
        kod (:class:`str`): Kod pracownika
        login_id (:class:`int`): ID konta pracownika
    """

    def __init__(self, id=None, imie=None, nazwisko=None, kod=None, login_id=None):
        self.id = id
        self.nazwa = "{!s} {!s}".format(nazwisko, imie)
        self.imie = imie
        self.nazwisko = nazwisko
        self.kod = kod
        self.login_id = login_id

    def __repr__(self):
        return "<Pracownik {!r}>".format(self.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        imie = j.get("Imie")
        nazwisko = j.get("Nazwisko")
        kod = j.get("Kod")
        login_id = j.get("LoginId")
        return cls(id=id, imie=imie, nazwisko=nazwisko, kod=kod, login_id=login_id)
