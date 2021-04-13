# -*- coding: utf-8 -*-
from typing import AsyncIterator, List, Union

from related import ChildField, IntegerField, SequenceField, StringField, immutable

from .._api_helper import FilterType
from .._endpoints import DATA_MESSAGE
from ..model import Attachment, DateTime, Serializable


@immutable
class Address(Serializable):
    """An address - "descriptor" used in the system containing the user's Login ID, his names and a hash of the data.

    :var str ~.login_id: login id
    :var str ~.address_name: address name
    :var str ~.address_hash: address hash
    :var str ~.initials: initials
    """

    login_id: int = IntegerField(key="LoginId")
    address_name: str = StringField(key="Address")
    address_hash: str = StringField(key="AddressHash")
    initials: str = StringField(key="Initials")


@immutable
class Message(Serializable):
    """A message.

    :var int ~.id: Message id
    :var str ~.subject: Subject of the message
    :var `~vulcan.hebe.model.DateTime` ~.sent_date: Date with time when the message was sent
    :var `~vulcan.hebe.model.DateTime` ~.read_date: Date with time when the message was read
    :var int ~.status: Message status
    :var str ~.content: Message content
    :var `~vulcan.data.Address` ~.sender: Sender of the message
    :var List[Address] ~.receivers: Receiver of the message
    :var List[Attachment] ~.attachments: attachments added to message
    """

    id: int = IntegerField(key="Id", required=False)
    subject: str = StringField(key="Subject", required=False)
    sent_date: DateTime = ChildField(DateTime, key="DateSent", required=False)
    read_date: DateTime = ChildField(DateTime, key="DateRead", required=False)
    status: int = IntegerField(key="Status", required=False)
    content: str = StringField(key="Content", required=False)
    sender: Address = ChildField(Address, key="Sender", required=False)
    receivers: List[Address] = SequenceField(
        Address, key="Receiver", repr=True, required=False
    )
    attachments: List[Attachment] = SequenceField(
        Attachment, key="Attachments", repr=True, required=False
    )

    @classmethod
    async def get(
        cls, api, last_sync, folder, **kwargs
    ) -> Union[AsyncIterator["Message"], List[int]]:
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Message`], List[int]]
        """
        data = await api.helper.get_list(
            DATA_MESSAGE,
            FilterType.BY_PERSON,
            last_sync=last_sync,
            folder=folder,
            **kwargs
        )

        for message in data:
            yield Message.load(message)
