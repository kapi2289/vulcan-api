# -*- coding: utf-8 -*-
from typing import AsyncIterator, List, Union

from related import (
    BooleanField,
    ChildField,
    IntegerField,
    SequenceField,
    StringField,
    immutable,
)

from .._api_helper import FilterType
from .._endpoints import DATA_HOMEWORK
from ..model import Attachment, DateTime, Serializable, Subject, Teacher


@immutable
class Homework(Serializable):
    """A homework.

    :var int ~.id: homework's external ID
    :var str ~.key: homework's key (UUID)
    :var int ~.homework_id: homework's internal ID
    :var str ~.content: homework's content
    :var `~vulcan.hebe.model.DateTime` ~.date_created: homework's creation date
    :var `~vulcan.hebe.model.Teacher` ~.creator: the teacher who added
        the homework
    :var `~vulcan.hebe.model.Subject` ~.subject: the homework's subject
    :var List[Attachment] ~.attachments: attachments added to homework
    :var bool ~.is_answer_required: Is an answer required
    :var `~vulcan.hebe.model.DateTime` ~.deadline: homework's date and time
    :var `~vulcan.hebe.model.DateTime` ~.answer_deadline: homework's answer deadline
    :var `~vulcan.hebe.model.DateTime` ~.answer_date: homework's answer date and time
    """

    id: int = IntegerField(key="Id")
    key: str = StringField(key="Key")
    homework_id: int = StringField(key="IdHomework")
    content: str = StringField(key="Content")
    date_created: DateTime = ChildField(DateTime, key="DateCreated")
    creator: Teacher = ChildField(Teacher, key="Creator")
    subject: Subject = ChildField(Subject, key="Subject")
    attachments: List[Attachment] = SequenceField(
        Attachment, key="Attachments", repr=True
    )
    is_answer_required: Subject = BooleanField(key="IsAnswerRequired")
    deadline: DateTime = ChildField(DateTime, key="Deadline")
    answer_deadline: DateTime = ChildField(
        DateTime, key="AnswerDeadline", required=False
    )
    answer_date: DateTime = ChildField(DateTime, key="AnswerDate", required=False)

    @classmethod
    async def get(
        cls, api, last_sync, deleted, **kwargs
    ) -> Union[AsyncIterator["Homework"], List[int]]:
        """
        :rtype: Union[AsyncIterator[:class:`~vulcan.hebe.data.Homework`], List[int]]
        """
        data = await api.helper.get_list(
            DATA_HOMEWORK,
            FilterType.BY_PUPIL,
            deleted=deleted,
            last_sync=last_sync,
            **kwargs
        )

        for homework in data:
            yield Homework.load(homework)
