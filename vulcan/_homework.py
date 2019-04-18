from ._employee import Pracownik
from ._subject import Przedmiot
from ._utils import timestamp_to_date


class ZadanieDomowe:
    """
    Zadanie domowe

    Attributes:
        id (:class:`int`): ID zadania domowego
        przedmiot (:class:`vulcan.models.Przedmiot`): Przedmiot, z którego jest zadane zadanie
        pracownik (:class:`vulcan.models.Pracownik`): Pracownik szkoły, który wpisał to zadanie
        opis (:class:`str`): Opis zadania domowego
        dzien (:class:`datetime.date`): Dzień zadania domowego
    """

    def __init__(self, id=None, pracownik=None, przedmiot=None, opis=None, dzien=None):
        self.id = id
        self.pracownik = pracownik
        self.przedmiot = przedmiot
        self.opis = opis
        self.dzien = dzien

    def __repr__(self):
        return "<ZadanieDomowe przedmiot={!r}>".format(self.przedmiot.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        pracownik = Pracownik.from_json(j.get("Pracownik"))
        przedmiot = Przedmiot.from_json(j.get("Przedmiot"))
        opis = j.get("Opis")
        dzien = timestamp_to_date(j.get("Data"))
        return cls(
            id=id, pracownik=pracownik, przedmiot=przedmiot, opis=opis, dzien=dzien
        )
