# -*- coding: utf-8 -*-
from typing import AsyncIterator, List, Union

from related import IntegerField, StringField, immutable

from .._endpoints import DATA_MESSAGEBOX
from ..model import Serializable


@immutable
class MessageBox(Serializable):
    """A message box (not a folder, but an account/person/recipient).

    :var int ~.id: MessageBox id
    :var str ~.global_key: MessageBox Global Key
    :var str ~.name: MessageBox name
    """

    id: int = IntegerField(key="Id")
    global_key: str = StringField(key="GlobalKey")
    name: str = StringField(key="Name")

    @classmethod
    async def get(cls, api, **kwargs) -> AsyncIterator["MessageBox"]:
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.MessageBox`]
        """
        data = await api.helper.get_list(DATA_MESSAGEBOX, None, **kwargs)

        for messagebox in data:
            yield MessageBox.load(messagebox)
