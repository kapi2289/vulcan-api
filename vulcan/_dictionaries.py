# -*- coding: utf-8 -*-

from related import immutable, SequenceField, to_model

from ._grade import GradeCategory
from ._lesson import LessonTime
from ._subject import Subject
from ._teacher import Teacher
from ._utils import find


@immutable
class Dictionaries:
    teachers_json = SequenceField(dict, key="Pracownicy")
    subjects_json = SequenceField(dict, key="Przedmioty")
    lesson_times_json = SequenceField(dict, key="PoryLekcji")
    grade_categories_json = SequenceField(dict, key="KategorieOcen")
    notice_categories_json = SequenceField(dict, key="KategorieUwag")
    attendance_categories_json = SequenceField(dict, key="KategorieFrekwencji")
    attendance_types_json = SequenceField(dict, key="TypyFrekwencji")

    @property
    def teachers(self):
        """list(:class:`vulcan._teacher.Teacher`): List of teachers"""
        return list(map(lambda j: to_model(Teacher, j), self.teachers_json))

    @property
    def subjects(self):
        """list(:class:`vulcan._subject.Subject`): List of subjects"""
        return list(map(lambda j: to_model(Subject, j), self.subjects_json))

    @property
    def lesson_times(self):
        """list(:class:`vulcan._lesson.LessonTime`): List of lesson times"""
        return list(map(lambda j: to_model(LessonTime, j), self.lesson_times_json))

    @property
    def grade_categories(self):
        """list(:class:`vulcan._grade.GradeCategory`): List of grade categories"""
        return list(
            map(lambda j: to_model(GradeCategory, j), self.grade_categories_json)
        )

    def get_teacher_json(self, _id):
        return find(self.teachers_json, _id)

    def get_teacher_by_login_id_json(self, _id):
        return find(self.teachers_json, _id, key="LoginId")

    def get_subject_json(self, _id):
        return find(self.subjects_json, _id)

    def get_lesson_time_json(self, _id):
        return find(self.lesson_times_json, _id)

    def get_grade_category_json(self, _id):
        return find(self.grade_categories_json, _id)

    def get_notice_category_json(self, _id):
        return find(self.notice_categories_json, _id)

    def get_attendance_category_json(self, _id):
        return find(self.attendance_categories_json, _id)

    def get_attendance_type_json(self, _id):
        return find(self.attendance_types_json, _id)

    @classmethod
    async def get(cls, api):
        j = await api.post("Uczen/Slowniki")
        return to_model(cls, j.get("Data"))
