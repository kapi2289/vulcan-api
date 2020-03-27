from datetime import datetime

from related import (
    IntegerField,
    StringField,
    DateField,
    ChildField,
    immutable,
    to_model,
)

from ._subject import Subject
from ._teacher import Teacher
from ._utils import sort_and_filter_date
@immutable
class Message:
	sender = StringField(key="Nadawca")
	senderid = StringField(key="NadawcaId")
	addressees = StringField(key="Adresaci")
	title = StringField(key="Tytul")
	content = StringField(key="Tresc")
	postdate = StringField(key="DataWyslania")
	posthour = StringField(key="GodzinaWyslania")
	folder= StringField(key="FolderWiadomosci")
	"""
	messageid = ChildField(MessageId, required=False)
	"""
	senderid = ChildField(Teacher, required=False)
	@classmethod
	def get(cls, api, date=None):
		if not date:
			date = datetime.now()
		date_str = date.strftime("%Y-%m-%d")

		date = {"DataPoczatkowa": "2020-01-01", "DataKoncowa": date_str}
		j = api.post("Uczen/WiadomosciOdebrane", json=date) 
		s1=j.get("Data", [])

		for message in s1:
			message["teacher"] = api.dict.get_teacher(message["NadawcaId"])
			yield to_model(cls, message)
	"""
	@classmethod
	def send(cls, api, name, title, content, adresses):
		 
		mesage={"NadawcaWiadomosci":name,"Tytul":title, "Tresc":content, "Adresaci":[{"Nazwa":adresses}]}
		print(name+title+content+adresses)
		print(name)
		sendmessage=api.post("Uczen/DodajWiadomosc", json=mesage, as_json=False)
		print(sendmessage)
	"""