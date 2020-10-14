# -*- coding: utf-8 -*-

from operator import itemgetter

from related import (
    IntegerField,
    immutable,
    StringField,
    DateField,
    ChildField,
    to_model,
)

from ._teacher import Teacher


@immutable
class NoticeType:
    """Notice type

    :var int ~.id: Notice type ID
    :var str ~.name: Name of the notice type
    """

    id = IntegerField(key="Id")
    name = StringField(key="Nazwa")


@immutable
class Notice:
    """Positive, negative or neutral student notice

    :var int ~.id: Notice ID
    :var str ~.content: Content of the notice
    :var `datetime.date` ~.date: Notice added date
    :var `~vulcan._notice.NoticeType` ~.type: Notice type class
    :var `~vulcan._teacher.Teacher` ~.teacher: Teacher, who added the notice
    """

    id = IntegerField(key="Id")
    content = StringField(key="TrescUwagi")
    date = DateField(key="DataWpisuTekst")

    type = ChildField(NoticeType, required=False)
    teacher = ChildField(Teacher, required=False)

    @classmethod
    def get(cls, api):
        j = api.post("Uczen/UwagiUcznia")

        notices = sorted(j.get("Data", []), key=itemgetter("DataWpisu"))

        for notice in notices:
            notice["type"] = api.dict.get_notice_category_json(
                notice["IdKategoriaUwag"]
            )
            notice["teacher"] = api.dict.get_teacher_json(notice["IdPracownik"])

            yield to_model(cls, notice)
