# -*- coding: utf-8 -*-

import io
import json
from typing import Type, TypeVar

from related import immutable, to_json, to_model

T = TypeVar("T")


@immutable
class Serializable:
    """A base class allowing to (de)serialize objects easily into
    appropriate class variables.
    """

    @property
    def as_json(self) -> str:
        """Serialize the object as a JSON string.

        :rtype: str
        """
        return to_json(self)

    @property
    def as_dict(self) -> dict:
        """Serialize the object as a dictionary.

        :rtype: dict
        """
        return json.loads(self.as_json)

    @classmethod
    def load(cls: Type[T], data) -> T:
        """Deserialize provided ``data`` into an instance of ``cls``.

        The ``data`` parameter may be:

        - a JSON string
        - a dictionary
        - a handle to a file containing a JSON string

        :param data: the data to deserialize
        """
        if not data:
            return None
        if isinstance(data, dict):
            return to_model(cls, data)
        elif isinstance(data, io.IOBase):
            return to_model(cls, json.load(data))
        elif isinstance(data, str):
            return to_model(cls, json.loads(data))
        else:
            raise ValueError("Unknown data type")
