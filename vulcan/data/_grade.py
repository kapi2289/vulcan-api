# -*- coding: utf-8 -*-
from typing import AsyncIterator, List, Union

from related import ChildField, FloatField, IntegerField, StringField, immutable

from .._api_helper import FilterType
from .._endpoints import DATA_GRADE
from ..model import DateTime, Period, Serializable, Subject, Teacher


@immutable
class GradeCategory(Serializable):
    """A base grade category. Represents a generic type, like an exam, a short test,
    a homework or other ("current") grades.

    :var int ~.id: grade category's ID
    :var str ~.name: grade category's name
    :var str ~.code: grade category's code (e.g. short name or abbreviation)
    """

    id: int = IntegerField(key="Id")
    name: str = StringField(key="Name")
    code: str = StringField(key="Code")


@immutable
class GradeColumn(Serializable):
    """A grade column. Represents a topic which a student
    may get a grade from (e.g. a single exam, short test, homework).

    :var int ~.id: grade column's ID
    :var str ~.key: grade column's key (UUID)
    :var int ~.period_id: ID of the period when the grade is given
    :var str ~.name: grade column's name (description)
    :var str ~.code: grade column's code (e.g. short name or abbreviation)
    :var str ~.group: unknown, yet
    :var int ~.number: unknown, yet
    :var int ~.weight: weight of this column's grades
    :var `~vulcan.model.Subject` ~.subject: the subject from which
        grades in this column are given
    :var `~vulcan.data.GradeCategory` ~.category: category (base type)
        of grades in this column
    :var `~vulcan.model.Period` ~.period: a resolved period of this grade
    """

    id: int = IntegerField(key="Id")
    key: str = StringField(key="Key")
    period_id: int = IntegerField(key="PeriodId")
    name: str = StringField(key="Name")
    code: str = StringField(key="Code")
    number: int = IntegerField(key="Number")
    weight: float = FloatField(key="Weight")
    subject: Subject = ChildField(Subject, key="Subject")
    group: str = StringField(key="Group", required=False)
    category: GradeCategory = ChildField(GradeCategory, key="Category", required=False)

    period: Period = ChildField(Period, key="Period", required=False)


@immutable
class Grade(Serializable):
    """A grade.

    :var int ~.id: grade's ID
    :var str ~.key: grade's key (UUID)
    :var int ~.pupil_id: the related pupil's ID
    :var str ~.content_raw: grade's content (with comment)
    :var str ~.content: grade's content (without comment)
    :var `~vulcan.model.DateTime` ~.date_created: grade's creation date
    :var `~vulcan.model.DateTime` ~.date_modified: grade's modification date
        (may be the same as ``date_created`` if it was never modified)
    :var `~vulcan.model.Teacher` ~.teacher_created: the teacher who added
        the grade
    :var `~vulcan.model.Teacher` ~.teacher_modified: the teacher who modified
        the grade
    :var `~vulcan.data.GradeColumn` ~.column: grade's column
    :var float ~.value: grade's value, may be `None` if 0.0
    :var str ~.comment: grade's comment, visible in parentheses in ``content_raw``
    :var float ~.numerator: for point grades: the numerator value
    :var float ~.denominator: for point grades: the denominator value
    """

    id: int = IntegerField(key="Id")
    key: str = StringField(key="Key")
    pupil_id: int = IntegerField(key="PupilId")
    content_raw: str = StringField(key="ContentRaw")
    content: str = StringField(key="Content")
    date_created: DateTime = ChildField(DateTime, key="DateCreated")
    date_modified: DateTime = ChildField(DateTime, key="DateModify")
    teacher_created: Teacher = ChildField(Teacher, key="Creator")
    teacher_modified: Teacher = ChildField(Teacher, key="Modifier")
    column: GradeColumn = ChildField(GradeColumn, key="Column")
    value: float = FloatField(key="Value", required=False)
    comment: str = StringField(key="Comment", required=False)
    numerator: float = FloatField(key="Numerator", required=False)
    denominator: float = FloatField(key="Denominator", required=False)

    @classmethod
    async def get(
        cls, api, last_sync, deleted, **kwargs
    ) -> Union[AsyncIterator["Grade"], List[int]]:
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Grade`], List[int]]
        """
        data = await api.helper.get_list(
            DATA_GRADE,
            FilterType.BY_PUPIL,
            deleted=deleted,
            last_sync=last_sync,
            **kwargs
        )

        for grade in data:
            grade["Column"]["Period"] = api.student.period_by_id(
                grade["Column"]["PeriodId"]
            ).as_dict
            yield Grade.load(grade)
