# -*- coding: utf-8 -*-
from typing import AsyncIterator, List, Union

from related import IntegerField, StringField, immutable

from .._endpoints import DATA_MESSAGEBOX
from ..model import Serializable


@immutable
class Messagebox(Serializable):
    """A messagebox.

    :var int ~.id: Messagebox id
    :var str ~.global_key: Messagebox Global Key
    :var str ~.name: Messagebox name
    """

    id: int = IntegerField(key="Id")
    global_key: str = StringField(key="GlobalKey")
    name: str = StringField(key="Name")

    @classmethod
    async def get(cls, api, **kwargs) -> Union[AsyncIterator["Messagebox"], List[int]]:
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Messagebox`], List[int]]
        """
        data = await api.helper.get_list(DATA_MESSAGEBOX, None, **kwargs)

        for messagebox in data:
            yield Messagebox.load(messagebox)
