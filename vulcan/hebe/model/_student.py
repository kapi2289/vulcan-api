# -*- coding: utf-8 -*-
from typing import List

from related import immutable, StringField, ChildField, SequenceField

from ._period import Period
from ._pupil import Pupil
from ._school import School
from ._serializable import Serializable
from ._unit import Unit
from .._endpoints import STUDENT_LIST


@immutable
class Student(Serializable):
    """A student object, along with his school, class and period information

    :var str ~.symbol: the "partition" symbol - can be a town or county name
    :var str ~.symbol_code: the school unit code - often a 6 digit number
    :var `~vulcan.hebe.model.Pupil` ~.pupil: contains the student's IDs,
         names and email
    :var `~vulcan.hebe.model.Unit` ~.unit: info about the school unit
         (e.g. several school buildings)
    :var `~vulcan.hebe.model.School` ~.school: info about the school
         (a single building of the unit)
    :var List[`~vulcan.hebe.model.Period`] ~.periods: a list of
         the student's school year periods
    """

    symbol: str = StringField(key="TopLevelPartition")
    symbol_code: str = StringField(key="Partition")

    pupil: Pupil = ChildField(Pupil, key="Pupil")
    unit: Unit = ChildField(Unit, key="Unit")
    school: School = ChildField(School, key="ConstituentUnit")
    periods: List[Period] = SequenceField(Period, key="Periods")

    @property
    def full_name(self) -> str:
        """Gets the student's full name in "FirstName SecondName LastName" format.

        :rtype: str
        """
        return " ".join(
            part
            for part in [
                self.pupil.first_name.strip(),
                self.pupil.second_name.strip(),
                self.pupil.last_name.strip(),
            ]
            if part
        )

    @property
    def current_period(self) -> Period:
        """Gets the currently ongoing period of the student.

        :rtype: :class:`~vulcan.hebe.model.Period`
        """
        return next((period for period in self.periods if period.current), None)

    def period_by_id(self, period_id: int) -> Period:
        """Gets a period matching the given period ID.

        :param int period_id: the period ID to look for
        :rtype: :class:`~vulcan.hebe.model.Period`
        """
        return next((period for period in self.periods if period.id == period_id), None)

    @classmethod
    async def get(cls, api, **kwargs) -> List["Student"]:
        """
        :rtype: List[:class:`~vulcan.hebe.model.Student`]
        """
        data = await api.get(STUDENT_LIST, **kwargs)
        return list(Student.load(student) for student in data)
