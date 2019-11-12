from __future__ import unicode_literals

from ._api import Api
from ._certificate import Certificate
from ._exam import Exam
from ._grade import Grade
from ._homework import Homework
from ._lesson import Lesson
from ._student import Student
from ._utils import log


class Vulcan:
    """
    Loguje się do dzienniczka za pomocą wygenerowanego certyfikatu

    Args:
        certificate (:class:`dict`): Certyfikat wygenerowany za pomocą :func:`vulcan.Vulcan.register`
    """

    def __init__(self, certificate, logging_level=None):
        self.api = Api(certificate)

        if logging_level:
            Vulcan.set_logging_level(logging_level)

        self.students = self.get_students()
        self.set_student(next(self.students))

    @staticmethod
    def set_logging_level(logging_level):
        """
        Ustawia poziom logowania

        Args:
            logging_level (:class:`int`): Poziom logowania z modułu :module:`logging`
        """

        log.setLevel(logging_level)

    @staticmethod
    def register(token, symbol, pin):
        """
        Rejestruje API jako nowe urządzenie mobilne

        Args:
            token (:class:`str`): Token
            symbol (:class:`str`): Symbol/Nazwa instancji
            pin (:class:`str`): Kod PIN

        Returns:
            :class:`dict`: Certyfikat
        """
        return Certificate.get(token, symbol, pin)

    def get_students(self):
        """
        Zwraca listę wszystkich uczniów należących do użytkownika

        Returns:
            :class:`list`: Listę uczniów
        """
        return Student.get(self.api)

    def set_student(self, student):
        """
        Ustawia domyślnego ucznia

        Args:
            uczen (:class:`vulcan.Student`): Jeden z uczniów zwróconych przez :func:`vulcan.Vulcan.uczniowie`
        """
        self.api.set_student(student)

    def get_grades(self):
        """
        Pobiera oceny cząstkowe

        Returns:
            :class:`list`: Listę ocen cząstkowych
        """
        return Grade.get(self.api)

    def get_lessons(self, date=None):
        """
        Pobiera plan lekcji z danego dnia

        Args:
            date (:class:`datetime.date` or :class:`datetime.datetime`): Dzień z którego pobrać plan
                lekcji, jeśli puste pobiera z aktualnego dnia

        Returns:
            :class:`list`: Listę lekcji
        """
        return Lesson.get(self.api, date)

    def get_exams(self, date=None):
        """
        Pobiera sprawdziany z danego dnia

        Args:
            date (:class:`datetime.date` or :class:`datetime.datetime`): Dzień z którego pobrać
                sprawdziany, jeśli puste pobiera z aktualnego dnia

        Returns:
            :class:`list`: Listę sprawdzianów
        """
        return Exam.get(self.api, date)

    def get_homework(self, date=None):
        """
        Pobiera zadania domowe z danego dnia

        Args:
            date (:class:`datetime.date` or :class:`datetime.datetime`): Dzień z którego pobrać
                zadania domowe, jeśli puste pobiera z aktualnego dnia

        Returns:
            :class:`list`: Listę zadań domowych
        """
        return Homework.get(self.api, date)
