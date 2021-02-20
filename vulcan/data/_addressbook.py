# -*- coding: utf-8 -*-
from typing import AsyncIterator, List, Union

from related import IntegerField, SequenceField, StringField, immutable

from .._api_helper import FilterType
from .._endpoints import DATA_ADDRESSBOOK
from ..model import Serializable


@immutable
class Role(Serializable):
    """A role of addressee.

    :var str ~.role_name: role name
    :var int ~.role_order: role order
    :var str ~.address_name: address name
    :var str ~.address_hash: address hash
    :var str ~.first_name: recipient's first name
    :var str ~.last_name: recipient's last name
    :var str ~.initials: recipient's initials
    :var str ~.unit_symbol: recipient's unit_symbol
    :var str ~.constituent_unit_symbol: recipient's constituent unit symbol
    :var str ~.class_symbol: recipient's class symbol
    """

    role_name: str = StringField(key="RoleName")
    role_order: int = IntegerField(key="RoleOrder")
    address_name: str = StringField(key="Address")
    address_hash: str = StringField(key="AddressHash")
    first_name: str = StringField(key="Name")
    last_name: str = StringField(key="Surname")
    initials: str = StringField(key="Initials")
    unit_symbol: str = StringField(key="UnitSymbol", required=False)
    constituent_unit_symbol: str = StringField(
        key="ConstituentUnitSymbol", required=False
    )
    class_symbol: str = StringField(key="ClassSymbol", required=False)


@immutable
class Addressbook(Serializable):
    """An address book.

    :var str ~.id: recipient id
    :var str ~.login_id: recipient login id
    :var str ~.first_name: recipient's first name
    :var str ~.last_name: recipient's last name
    :var str ~.initials: recipient's initials
    :var list[Role] ~.roles: recipient's role (eg. Teacher)
    """

    id: str = StringField(key="Id")
    login_id: int = IntegerField(key="LoginId")
    first_name: str = StringField(key="Name")
    last_name: str = StringField(key="Surname")
    initials: str = StringField(key="Initials")

    roles: List[Role] = SequenceField(Role, key="Roles", repr=True)

    @classmethod
    async def get(cls, api, **kwargs) -> Union[AsyncIterator["Addressbook"], List[int]]:
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Addressbook`], List[int]]
        """
        data = await api.helper.get_list(
            DATA_ADDRESSBOOK, FilterType.BY_LOGIN_ID, **kwargs
        )

        for addressbook in data:
            yield Addressbook.load(addressbook)
