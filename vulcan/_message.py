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
	def get(cls, api, date=None):
		if not date:
			date=api.student.period.from_
		date_first=date.strftime("%Y-%m-%d")
		date_last=api.student.period.to.strftime("%Y-%m-%d")
		data = {"DataPoczatkowa": date_first, "DataKoncowa": date_last}
		j = api.post("Uczen/WiadomosciOdebrane", json=data) 
		messages=j.get("Data", [])

		for message in messages:
			message["sender"] = api.dict.get_teacher(message["NadawcaId"])
			yield to_model(cls, message)