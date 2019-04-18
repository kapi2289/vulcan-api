from aenum import Enum, unique

from ._employee import Pracownik
from ._subject import Przedmiot
from ._utils import timestamp_to_date


@unique
class RodzajSprawdzianu(Enum):
    """
    Rodzaj sprawdzianu

    Todo:
        Dodać enum testu
    """

    SPRAWDZIAN = 1
    KARTKOWKA = 2
    PRACA_KLASOWA = 3


class Sprawdzian:
    """
    Sprawdzian, test, praca klasowa lub kartkówka

    Attributes:
        id (:class:`int`): ID sprawdzianu
        rodzaj (:class:`vulcan.models.RodzajSprawdzianu`): Rodzaj sprawdzianu
        przedmiot (:class:`vulcan.models.Przedmiot`): Przedmiot, z którego jest sprawdzian
        pracownik (:class:`vulcan.models.Pracownik`): Pracownik szkoły, który wpisał sprawdzian
        opis (:class:`str`): Opis sprawdzianu
        dzien (:class:`datetime.date`): Dzień sprawdzianu
    """

    def __init__(
        self,
        id=None,
        rodzaj=None,
        przedmiot=None,
        pracownik=None,
        opis=None,
        dzien=None,
    ):
        self.id = id
        self.rodzaj = rodzaj
        self.przedmiot = przedmiot
        self.pracownik = pracownik
        self.opis = opis
        self.dzien = dzien

    def __repr__(self):
        return "<Sprawdzian: przedmiot={!r}>".format(self.przedmiot.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        rodzaj = RodzajSprawdzianu(j.get("RodzajNumer"))
        przedmiot = Przedmiot.from_json(j.get("Przedmiot"))
        pracownik = Pracownik.from_json(j.get("Pracownik"))
        opis = j.get("Opis")
        dzien = timestamp_to_date(j.get("Data"))
        return cls(
            id=id,
            rodzaj=rodzaj,
            przedmiot=przedmiot,
            pracownik=pracownik,
            opis=opis,
            dzien=dzien,
        )
