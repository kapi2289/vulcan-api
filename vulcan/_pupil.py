from aenum import Enum, unique

from ._class import Klasa
from ._period import Okres
from ._school import Szkola


@unique
class Plec(Enum):
    """Płeć"""

    KOBIETA = 0
    MEZCZYZNA = 1


class Uczen:
    """
    Uczeń

    Attributes:
        id (:class:`int`): ID ucznia
        nazwa (:class:`str`): Nazwisko, imię oraz drugie imię ucznia
        imie (:class:`str`): Pierwsze imię ucznia
        drugie_imie (:class:`str` or :class:`None`): Drugie imię ucznia
        nazwisko (:class:`str`): Nazwisko ucznia
        pseudonim (:class:`str` or :class:`None`): Pseudonim ucznia
        plec (:class:`vulcan.models.Plec`): Płeć ucznia
        okres (:class:`vulcan.models.Okres`): Aktualny okres klasyfikacyjny ucznia
        klasa (:class:`vulcan.models.Klasa`): Klasa ucznia
        szkola (:class:`vulcan.models.Szkola`): Szkoła ucznia
    """

    def __init__(
        self,
        id=None,
        login_id=None,
        nazwa=None,
        imie=None,
        drugie_imie=None,
        nazwisko=None,
        pseudonim=None,
        plec=None,
        okres=None,
        klasa=None,
        szkola=None,
    ):
        self.id = id
        self.login_id = login_id
        self.nazwa = nazwa
        self.imie = imie
        self.drugie_imie = drugie_imie
        self.nazwisko = nazwisko
        self.pseudonim = pseudonim
        self.plec = plec
        self.okres = okres
        self.klasa = klasa
        self.szkola = szkola

    def __repr__(self):
        return "<Uczen {!r}>".format(self.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        login_id = j.get("UzytkownikLoginId")
        nazwa = j.get("UzytkownikNazwa")
        imie = j.get("Imie")
        drugie_imie = j.get("Imie2") or None
        nazwisko = j.get("Nazwisko")
        pseudonim = j.get("Pseudonim")
        plec = Plec(j.get("UczenPlec"))
        okres = Okres.from_json(j)
        klasa = Klasa.from_json(j)
        szkola = Szkola.from_json(j)
        return cls(
            id=id,
            login_id=login_id,
            nazwa=nazwa,
            imie=imie,
            drugie_imie=drugie_imie,
            nazwisko=nazwisko,
            pseudonim=pseudonim,
            plec=plec,
            okres=okres,
            klasa=klasa,
            szkola=szkola,
        )
