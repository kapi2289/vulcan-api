# -*- coding: utf-8 -*-

from related import immutable, StringField, ChildField, SequenceField
from ._serializable import Serializable
from .._endpoints import STUDENT_LIST

from ._pupil import Pupil
from ._unit import Unit
from ._school import School
from ._period import Period


@immutable
class Student(Serializable):
    symbol = StringField(key="TopLevelPartition")
    symbol_code = StringField(key="Partition")

    pupil = ChildField(Pupil, key="Pupil")
    unit = ChildField(Unit, key="Unit")
    school = ChildField(School, key="ConstituentUnit")
    periods = SequenceField(Period, key="Periods")

    # pylint: disable=E1101
    @property
    def full_name(self) -> str:
        return " ".join(
            part
            for part in [
                self.pupil.first_name.strip(),
                self.pupil.second_name.strip(),
                self.pupil.last_name.strip(),
            ]
            if part
        )

    @classmethod
    def get(cls, api):
        data = api.get(STUDENT_LIST)

        for student in data:
            yield Student.load(student)
