from ._employee import Pracownik
from ._subject import Przedmiot
from ._utils import timestamp_to_datetime, concat_hours_and_minutes


class PoraLekcji:
    """
    Pora lekcji

    Attributes:
        id (:class:`int`): ID pory lekcji
        numer (:class:`int`): Numer kolejny pory lekcji
        od (:class:`datetime.datetime`): Godzina i minuta rozpoczęcia lekcji
        do (:class:`datetime.datetime`): Godzina i minuta zakończenia lekcji
    """

    def __init__(self, id=None, numer=None, od=None, do=None):
        self.id = id
        self.numer = numer
        self.od = od
        self.do = do

    def __repr__(self):
        return "<PoraLekcji {!s}: od='{!s}:{:02d}' do='{!s}:{:02d}'>".format(
            self.numer, self.od.hour, self.od.minute, self.do.hour, self.do.minute
        )

    @classmethod
    def from_json(cls, j):
        id = j.get("Id")
        numer = j.get("Numer")
        od = timestamp_to_datetime(j.get("Poczatek"))
        do = timestamp_to_datetime(j.get("Koniec"))
        return cls(id=id, numer=numer, od=od, do=do)


class Lekcja:
    """
    Lekcja

    Attributes:
        numer (:class:`int`): Numer lekcji
        pora (:class:`vulcan.models.PoraLekcji`): Informacje o porze lekcji
        przedmiot (:class:`vulcan.models.Przedmiot`): Przedmiot na lekcji
        dzien (:class:`datetime.date`): Data lekcji
        od (:class:`datetime.datetime`): Data i godzina rozpoczęcia lekcji
        do (:class:`datetime.datetime`): Data i godzina zakończenia lekcji
    """

    def __init__(
        self,
        numer=None,
        pora=None,
        przedmiot=None,
        pracownik=None,
        dzien=None,
        od=None,
        do=None,
    ):
        self.numer = numer
        self.pora = pora
        self.przedmiot = przedmiot
        self.pracownik = pracownik
        self.dzien = dzien
        self.od = od
        self.do = do

    def __repr__(self):
        return "<Lekcja {!s}: przedmiot={!r} pracownik={!r}>".format(
            self.numer, self.przedmiot.nazwa, self.pracownik.nazwa
        )

    @classmethod
    def from_json(cls, j):
        numer = j.get("NumerLekcji")
        pora = PoraLekcji.from_json(j.get("PoraLekcji"))
        przedmiot = Przedmiot.from_json(j.get("Przedmiot"))
        pracownik = Pracownik.from_json(j.get("Pracownik"))
        dzien_datetime = timestamp_to_datetime(j.get("Dzien"))
        dzien = dzien_datetime.date()
        od = concat_hours_and_minutes(dzien_datetime, j["PoraLekcji"]["Poczatek"])
        do = concat_hours_and_minutes(dzien_datetime, j["PoraLekcji"]["Koniec"])
        return cls(
            numer=numer,
            pora=pora,
            przedmiot=przedmiot,
            pracownik=pracownik,
            dzien=dzien,
            od=od,
            do=do,
        )
