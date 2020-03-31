# -*- coding: utf-8 -*-

from datetime import datetime

from related import (
	TimeField,
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
	id = IntegerField(key="WiadomoscId")
	sender_id = StringField(key="NadawcaId")
	recipients = StringField(key="Adresaci")
	title = StringField(key="Tytul")
	content = StringField(key="Tresc")
	sent_data = StringField(key="DataWyslania")
	sent_time = StringField(key="GodzinaWyslania")
	folder= StringField(key="FolderWiadomosci")
	sender = ChildField(Teacher, required=False)
	@classmethod
	def get(cls, api, date_from=None, date_to=None):
		if not date_from:
			date_from=api.student.period.from_
		if not date_to:
			date_to=api.student.period.to
		date_from_str=date_from.strftime("%Y-%m-%d")
		date_to_str=date_to.strftime("%Y-%m-%d")
		data = {"DataPoczatkowa": date_from_str, "DataKoncowa": date_to_str}
		j = api.post("Uczen/WiadomosciOdebrane", json=data) 
		messages=j.get("Data", [])

		for message in messages:
			message["sender"] = api.dict.get_teacher(message["NadawcaId"])
			yield to_model(cls, message)
	def send(api, name, title, content, recipient_id, recipients):
		data = {"NadawcaWiadomosci": name, "Tytul": title, "Tresc": content, "Adresaci":[{"LoginId": recipient_id, "Nazwa": recipients}]}
		j = api.post("Uczen/DodajWiadomosc", json=data)
