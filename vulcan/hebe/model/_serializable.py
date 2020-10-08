# -*- coding: utf-8 -*-

import io, json
from related import immutable, to_model, to_json


@immutable
class Serializable:
    @property
    def as_json(self):
        return to_json(self)

    @property
    def as_dict(self):
        return json.loads(self.as_json)

    @classmethod
    def load(cls, data):
        if isinstance(data, dict):
            return to_model(cls, data)
        elif isinstance(data, io.IOBase):
            return to_model(cls, json.load(data))
        elif isinstance(data, str):
            return to_model(cls, json.loads(data))
        else:
            raise ValueError("Unknown data type")
