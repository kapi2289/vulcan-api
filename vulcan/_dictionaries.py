from related import immutable, SequenceField

from _utils import find


@immutable
class Dictionaries:
    teachers = SequenceField(dict, key="Pracownicy")
    subjects = SequenceField(dict, key="Przedmioty")
    lesson_times = SequenceField(dict, key="PoryLekcji")
    grade_categories = SequenceField(dict, key="KategorieOcen")
    notice_categories = SequenceField(dict, key="KategorieUwag")
    attendance_categories = SequenceField(dict, key="KategorieFrekwencji")
    attendance_types = SequenceField(dict, key="TypyFrekwencji")

    def get_teacher(self, _id):
        return find(self.teachers, _id)

    def get_subject(self, _id):
        return find(self.subjects, _id)

    def get_lesson_time(self, _id):
        return find(self.lesson_times, _id)

    def get_grade_category(self, _id):
        return find(self.grade_categories, _id)

    def get_notice_category(self, _id):
        return find(self.notice_categories, _id)

    def get_attendance_category(self, _id):
        return find(self.attendance_categories, _id)

    def get_attendance_type(self, _id):
        return find(self.attendance_types, _id)
