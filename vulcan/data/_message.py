# -*- coding: utf-8 -*-
from typing import AsyncIterator, List, Union

from related import ChildField, IntegerField, SequenceField, StringField, immutable

from .._api_helper import FilterType
from .._endpoints import DATA_MESSAGE
from ..model import Attachment, DateTime, Serializable


@immutable
class Address(Serializable):
    """An address - "descriptor" used in the system containing the user's Global Key, his names and a information whether the user has read the message.

    :var str ~.global_key: Global Key
    :var str ~.name: address name
    :var int ~.has_read: whether the user has read the message
    """

    global_key: str = StringField(key="GlobalKey")
    name: str = StringField(key="Name")
    has_read: int = IntegerField(key="HasRead", required=False)


@immutable
class Message(Serializable):
    """A message.

    :var str ~.id: Message id
    :var str ~.global_key: Message Global Key
    :var str ~.thread_key: Message thread key
    :var str ~.subject: Subject of the message
    :var str ~.content: Message content
    :var `~vulcan.hebe.model.DateTime` ~.sent_date: Date with time when the message was sent
    :var `~vulcan.hebe.model.DateTime` ~.read_date: Date with time when the message was read
    :var int ~.status: Message status
    :var `~vulcan.data.Address` ~.sender: Sender of the message
    :var List[Address] ~.receivers: Receiver of the message
    :var List[Attachment] ~.attachments: attachments added to message
    """

    id: str = StringField(key="Id")
    global_key: str = StringField(key="GlobalKey")
    thread_key: str = StringField(key="ThreadKey")
    subject: str = StringField(key="Subject")
    content: str = StringField(key="Content")
    sent_date: DateTime = ChildField(DateTime, key="DateSent")
    status: int = IntegerField(key="Status")
    sender: Address = ChildField(Address, key="Sender")
    receivers: List[Address] = SequenceField(Address, key="Receiver", repr=True)
    attachments: List[Attachment] = SequenceField(
        Attachment, key="Attachments", repr=True
    )
    read_date: DateTime = ChildField(DateTime, key="DateRead", required=False)

    @classmethod
    async def get(
        cls, api, message_box, last_sync, folder, **kwargs
    ) -> Union[AsyncIterator["Message"], List[int]]:
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Message`], List[int]]
        """
        data = await api.helper.get_list(
            DATA_MESSAGE,
            FilterType.BY_MESSAGEBOX,
            message_box=message_box,
            last_sync=last_sync,
            folder=folder,
            **kwargs
        )

        for message in data:
            yield Message.load(message)
