from ._employee import Pracownik
from ._subject import Przedmiot
from ._utils import timestamp_to_datetime


class KategoriaOceny:
    """
    Kategoria oceny

    Attributes:
        id (:class:`id`): Id kategorii
        kod (:class:`str`): Kod/skrót kategorii
        nazwa (:class:`str`): Pełna nazwa kategorii
    """

    def __init__(self, id=None, kod=None, nazwa=None):
        self.id = id
        self.kod = kod
        self.nazwa = nazwa

    def __repr__(self):
        return "<KategoriaOceny {!s}: {!s}>".format(self.kod, self.nazwa)

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        kod = j.get("Kod")
        nazwa = j.get("Nazwa")
        return cls(id=id, kod=kod, nazwa=nazwa)


class Ocena:
    """
    Ocena cząstkowa

    Attributes:
        id (:class:`int`): ID oceny
        pracownik (:class:`vulcan.models.Pracownik`): Pracownik, który wpisał ocenę
        przedmiot (:class:`vulcan.models.Przedmiot`): Przedmiot, z którego dostano ocenę
        kategoria (:class:`vulcan.models.KategoriaOceny`): Kategoria oceny
        wpis (:class:`str`): Wpis oceny
        wartosc (:class:`float`): Wartość oceny (przydaytna do obliczania średniej)
        waga (:class:`float`): Waga oceny
        opis (:class:`str`): Opis oceny
        data (:class:`datetime.datetime`): Data wpisania oceny
        data_modyfikacji (:class:`datetime.datetime`): Data ostatniej modyfikacji oceny
    """

    def __init__(
        self,
        id=None,
        pracownik=None,
        przedmiot=None,
        kategoria=None,
        wpis=None,
        wartosc=None,
        waga=None,
        opis=None,
        data=None,
        data_modyfikacji=None,
    ):
        self.id = id
        self.pracownik = pracownik
        self.przedmiot = przedmiot
        self.kategoria = kategoria
        self.wpis = wpis
        self.wartosc = wartosc
        self.waga = waga
        self.opis = opis
        self.data = data
        self.data_modyfikacji = data_modyfikacji

    def __repr__(self):
        return "<Ocena {!s}: waga={!r} przedmiot={!r}>".format(
            self.wpis, self.waga, self.przedmiot
        )

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        pracownik = Pracownik.from_json(j.get("Pracownik"))
        przedmiot = Przedmiot.from_json(j.get("Przedmiot"))
        if (j.get("Kategoria")):
            kategoria = KategoriaOceny.from_json(j.get("Kategoria"))
        else:
            kategoria = None
        wpis = j.get("Wpis")
        wartosc = j.get("Wartosc")
        waga = j.get("WagaOceny")
        opis = j.get("Opis")
        data = timestamp_to_datetime(j.get("DataUtworzenia"))
        data_modyfikacji = timestamp_to_datetime(j.get("DataModyfikacji"))
        return cls(
            id=id,
            pracownik=pracownik,
            przedmiot=przedmiot,
            kategoria=kategoria,
            wpis=wpis,
            wartosc=wartosc,
            waga=waga,
            opis=opis,
            data=data,
            data_modyfikacji=data_modyfikacji,
        )
