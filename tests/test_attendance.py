# -*- coding: utf-8 -*-

import pytest

from .utils import PARAMS_ATTENDANCE


@pytest.mark.online
@pytest.mark.parametrize("attendance_expected_list", PARAMS_ATTENDANCE)
class TestAttendance:
    def test(self, client, attendance_expected_list):
        attendance_list = client.get_attendance()
        for attendance_expected in attendance_expected_list:
            attendance = next(attendance_list)
            assert attendance.category.id == attendance_expected["IdKategoria"]
            assert attendance.time.number == attendance_expected["Numer"]
            assert attendance.time.id == attendance_expected["IdPoraLekcji"]
            assert attendance.subject.id == attendance_expected["IdPrzedmiot"]
            assert attendance.subject.name == attendance_expected["PrzedmiotNazwa"]
