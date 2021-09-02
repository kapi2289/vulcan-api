# -*- coding: utf-8 -*-
from typing import AsyncIterator, List, Union

from related import ChildField, IntegerField, StringField, immutable

from .._api_helper import FilterType
from .._endpoints import DATA_EXAM
from ..model import DateTime, Serializable, Subject, Teacher, TeamClass, TeamVirtual


@immutable
class Exam(Serializable):
    """An exam or short quiz.

    :var int ~.id: exam's ID
    :var str ~.key: exam's key (UUID)
    :var str ~.type: exam's type
    :var str ~.topic: exam's topic
    :var `~vulcan.model.DateTime` ~.date_created: exam's creation date
    :var `~vulcan.model.DateTime` ~.date_modified: exam's modification date
        (may be the same as ``date_created`` if it was never modified)
    :var `~vulcan.model.DateTime` ~.deadline: exam's date and time
    :var `~vulcan.model.Teacher` ~.creator: the teacher who added
        the exam
    :var `~vulcan.model.Subject` ~.subject: the exam's subject
    :var `~vulcan.model.TeamClass` ~.team_class: the class taking the exam
    :var `~vulcan.model.TeamVirtual` ~.team_virtual: the class distribution
        taking the exam, optional
    """

    id: int = IntegerField(key="Id")
    key: str = StringField(key="Key")
    type: str = StringField(key="Type")
    topic: str = StringField(key="Content")
    date_created: DateTime = ChildField(DateTime, key="DateCreated")
    date_modified: DateTime = ChildField(DateTime, key="DateModify")
    deadline: DateTime = ChildField(DateTime, key="Deadline")
    creator: Teacher = ChildField(Teacher, key="Creator")
    subject: Subject = ChildField(Subject, key="Subject")
    team_class: TeamClass = ChildField(TeamClass, key="Class", required=False)
    team_virtual: TeamVirtual = ChildField(
        TeamVirtual, key="Distribution", required=False
    )

    @classmethod
    async def get(
        cls, api, last_sync, deleted, **kwargs
    ) -> Union[AsyncIterator["Exam"], List[int]]:
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.data.Exam`], List[int]]
        """
        data = await api.helper.get_list(
            DATA_EXAM,
            FilterType.BY_PUPIL,
            deleted=deleted,
            last_sync=last_sync,
            **kwargs
        )

        for exam in data:
            yield Exam.load(exam)
