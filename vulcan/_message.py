# -*- coding: utf-8 -*-
from datetime import datetime

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
from ._utils import (
    log,
)


@immutable
class MessageRecipient:
    """Message recipient

    :var int ~.login_id: Recipient's login ID
    :var str ~.name: Recipient's name
    """

    login_id = IntegerField(key="LoginId")
    name = StringField(key="Nazwa")


@immutable
class Message:
    """Message

    :var int ~.id: Message ID
    :var int ~.sender_id: Message sender's (teacher) ID
    :var list ~.recipients: A list of :class:`vulcan._message.MessageRecipient` objects
    :var str ~.title: Title (subject) of the message
    :var str ~.content: Message content
    :var `~vulcan._teacher.Teacher` ~.sender: Sender of the message (teacher)
    :var `datetime.datetime` ~.sent_datetime: Date with time when the message was sent
    :var `datetime.date` ~.sent_date: Date when the message was sent
    :var `datetime.time` ~.sent_time: Time when the message was sent
    :var `datetime.datetime` ~.read_datetime: Date with time when the message was read, optional
    :var `datetime.date` ~.read_date: Date when the message was read, optional
    :var `datetime.time` ~.read_time: Time when the message was read, optional
    :var bool ~.is_read: Whether the message is read
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
        return datetime.combine(self.sent_date, self.sent_time)

    @property
    def read_datetime(self):
        if self.read_date and self.read_time:
            return datetime.combine(self.read_date, self.read_time)
        return None

    @property
    def is_read(self):
        return self.read_date is not None

    @classmethod
    def get(cls, api, date_from=None, date_to=None):
        if not date_from:
            date_from = api.student.period.from_
        if not date_to:
            date_to = api.student.period.to

        data = {
            "DataPoczatkowa": date_from.strftime("%Y-%m-%d"),
            "DataKoncowa": date_to.strftime("%Y-%m-%d"),
        }

        j = api.post("Uczen/WiadomosciOdebrane", json=data)

        messages = j.get("Data", [])

        for message in messages:
            message["sender"] = api.dict.get_teacher_by_login_id_json(
                message["NadawcaId"]
            )
            yield to_model(cls, message)

    @classmethod
    def send(cls, api, title, content, teachers):
        recipients = list()
        for teacher_repr in teachers:
            if isinstance(teacher_repr, int) or (
                isinstance(teacher_repr, str) and teacher_repr.isnumeric()
            ):
                teacher = to_model(
                    Teacher, api.dict.get_teacher_json(int(teacher_repr))
                )
            elif isinstance(teacher_repr, str):
                teacher = to_model(
                    Teacher, api.dict.get_teacher_by_name_json(teacher_repr)
                )
            elif isinstance(teacher_repr, Teacher):
                teacher = teacher_repr
            else:
                continue

            recipients.append(
                {
                    "LoginId": teacher.login_id,
                    "Nazwa": teacher.name_reversed,
                }
            )

        if len(recipients) == 0:
            raise ValueError("There must be at least 1 correct recipient.")

        data = {
            "NadawcaWiadomosci": api.student.account_name,
            "Tytul": title,
            "Tresc": content,
            "Adresaci": recipients,
        }

        log.info("Sending a message...")
        api.post("Uczen/DodajWiadomosc", json=data)
        log.info("Message sent successfully!")
