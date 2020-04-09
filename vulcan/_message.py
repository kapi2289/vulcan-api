# -*- coding: utf-8 -*-
from related import (
    IntegerField,
    StringField,
    ChildField,
    immutable,
    to_model,
    SequenceField,
    DateField,
    TimeField,
)

from ._teacher import Teacher


@immutable
class MessageRecipient:
    login_id = IntegerField(key="LoginId")
    name = StringField(key="Nazwa")


@immutable
class Message:
    """
    Attributes:
        id (:class:`int`): Message ID
        sender_id (:class:`int`) Message sender's (teacher) ID
        recipients (:class:`list`) List of :class:`vulcan._message.MessageRecipient` objects
        title (:class:`str`) Title (subject) of the message
        content (:class:`str`) Message content
        sender (:class:`vulcan._teacher.Teacher`) Sender of the message (teacher)
        sent_date (:class:`datetime.datetime`) Date when the message was sent
        sent_time (:class:`datetime.time`) Time when the message was sent
        sent_datetime (:class:`datetime.date`): Date with time when the message was sent
        read_date (:class:`datetime.datetime`) Date when the message was read
        read_time (:class:`datetime.time`) Time when the message was read
        read_datetime (:class:`datetime.date`): Date with time when the message was read
        is_read(:class:`bool`) Whether the message is read
    """

    id = IntegerField(key="WiadomoscId")
    sender_id = IntegerField(key="NadawcaId")
    recipients = SequenceField(MessageRecipient, key="Adresaci")
    title = StringField(key="Tytul")
    content = StringField(key="Tresc")
    sent_date = DateField(key="DataWyslania", formatter="%d.%m.%Y")
    sent_time = TimeField(key="GodzinaWyslania", formatter="%H:%M")
    read_date = DateField(key="DataPrzeczytania", formatter="%d.%m.%Y", required=False)
    read_time = TimeField(key="GodzinaPrzeczytania", formatter="%H:%M", required=False)

    sender = ChildField(Teacher, required=False)

    @property
    def sent_datetime(self):
        return self._sent_date.combine(self._sent_time)

    @property
    def read_datetime(self):
        if self._read_date and self._read_time:
            return self._read_date.combine(self._read_time)
        return None

    @property
    def is_read(self):
        return self.read_datetime is not None

    @classmethod
    async def get(cls, api, date_from=None, date_to=None):
        if not date_from:
            date_from = api.student.period.from_
        if not date_to:
            date_to = api.student.period.to
        date_from_str = date_from.strftime("%Y-%m-%d")
        date_to_str = date_to.strftime("%Y-%m-%d")

        data = {"DataPoczatkowa": date_from_str, "DataKoncowa": date_to_str}
        j = await api.post("Uczen/WiadomosciOdebrane", json=data)
        messages = j.get("Data", [])

        for message in messages:
            message["sender"] = api.dict.get_teacher_by_login_id_json(
                message["NadawcaId"]
            )
            yield to_model(cls, message)
