# -*- coding: utf-8 -*-

import pytest

from .utils import PARAMS_MESSAGE_LIST


@pytest.mark.private
@pytest.mark.parametrize("date, message_expected_list", PARAMS_MESSAGE_LIST)
class TestMessage:
    @pytest.mark.online
    def test(self, client, date, message_expected_list):
        messages_list = client.get_message(date)

        for message in messages_list:
            assert message.date == date

    def test_private(self, client, date, message_expected_list):
        message_list = client.get_message(date)

        for i, message in enumerate(message_list):
            message_expected = message_expected_list[i]
            assert message.id == message_expected["WiadomoscId"]
            assert message.subject.id == message_expected["IdPrzedmiot"]
            assert message.teacher.id == message_expected["IdPracownik"]
