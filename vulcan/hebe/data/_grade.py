# -*- coding: utf-8 -*-

from related import immutable, IntegerField, StringField, FloatField, ChildField

from ..model import Serializable, DateTime, Teacher


@immutable
class Grade(Serializable):
    """A grade.

    :var int ~.id: the period ID
    :var int ~.pupil_id: the related pupil ID
    """

    id = IntegerField(key="Id")
    pupil_id = IntegerField(key="PupilId")
    content_raw = StringField(key="ContentRaw")
    content = StringField(key="Content")
    date_created = ChildField(DateTime, key="DateCreated")
    date_modified = ChildField(DateTime, key="DateModify")
    teacher_created = ChildField(Teacher, key="Creator")
    teacher_modified = ChildField(Teacher, key="Modifier")
    value = FloatField(key="Value", required=False)
    comment = StringField(key="Comment", required=False)
    numerator = FloatField(key="Numerator", required=False)
    denominator = FloatField(key="Denominator", required=False)
