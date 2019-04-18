from ._utils import timestamp_to_date


class Okres:
    """
    Okres kwalifikacyjny

    Attributes:
        id (:class:`int`): ID okresu kwalifikacyjnego
        poziom (:class:`int`): Poziom (klasa) okresu kwalifikacyjnego
        numer (:class:`int`): Liczba kolejna okresu kwalifikacyjnego
        od (:class:`datetime.date`): Data rozpoczęcia okresu kwalifikacyjnego
        do (:class:`datetime.date`): Data zakończenia okresu kwalifikacyjnego
    """

    def __init__(self, id=None, poziom=None, numer=None, od=None, do=None):
        self.id = id
        self.poziom = poziom
        self.numer = numer
        self.od = od
        self.do = do

    def __repr__(self):
        return "<Okres: od={!r} do={!r}>".format(str(self.od), str(self.do))

    @classmethod
    def from_json(cls, j):
        id = j.get("IdOkresKlasyfikacyjny")
        poziom = j.get("OkresPoziom")
        numer = j.get("OkresNumer")
        od = timestamp_to_date(j["OkresDataOd"]) if j.get("OkresDataOd") else None
        do = timestamp_to_date(j["OkresDataDo"]) if j.get("OkresDataDo") else None
        return cls(id=id, poziom=poziom, numer=numer, od=od, do=do)
