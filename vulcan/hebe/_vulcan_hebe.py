# -*- coding: utf-8 -*-

from ._api import Api
from .model._student import Student
from ._utils_hebe import log


class VulcanHebe:
    def __init__(self, keystore, account, logging_level: int = None):
        self._api = Api(keystore, account)

        if logging_level:
            VulcanHebe.set_logging_level(logging_level)

    @staticmethod
    def set_logging_level(logging_level: int):
        """
        Sets the default logging level

        Args:
            logging_level (:class:`int`): Logging level from :module:`logging` module
        """

        log.setLevel(logging_level)

    def get_students(self):
        """
        Yields students that are assigned to the account

        Yields:
            :class:`vulcan.hebe._student.Student`
        """
        return Student.get(self._api)
