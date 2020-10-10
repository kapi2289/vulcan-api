# -*- coding: utf-8 -*-

from related import immutable, IntegerField, StringField


@immutable
class Teacher:
    """School teacher or employee

    :param int id: Teacher ID
    :param str first_name: Teacher first name
    :param str last_name: Teacher last name (surname)
    :param str short: Code (short name) of the teacher
    :param int login_id: Teacher account ID
    """

    id = IntegerField(key="Id")
    first_name = StringField(key="Imie")
    last_name = StringField(key="Nazwisko")
    short = StringField(key="Kod")
    login_id = IntegerField(key="LoginId")

    @property
    def name(self):
        """Returns the teacher's full name as "Name Surname".

        :rtype: str
        """
        return "{} {}".format(self.first_name, self.last_name)
