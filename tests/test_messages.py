# -*- coding: utf-8 -*-

import pytest

from .utils import PARAMS_MESSAGES


@pytest.mark.online
@pytest.mark.parametrize("messages_expected", PARAMS_MESSAGES)
class TestMessages:
    def test_private(self, client, messages_expected):
        messages = client.get_messages()

        for message_expected in messages_expected:
            message = next(
                filter(lambda m: m.id == message_expected["WiadomoscId"], messages)
            )

            assert message.id == message_expected["WiadomoscId"]
            if message.sender:
                assert (
                    message.sender.login_id
                    == message.sender_id
                    == message_expected["NadawcaId"]
                )
            assert message.title == message_expected["Tytul"]
            assert message_expected["Tresc"] in message.content
            if message.sent_date:
                assert (
                    message.sent_date.strftime("%d.%m.%Y")
                    == message_expected["DataWyslania"]
                )
            else:
                assert message_expected["DataWyslania"] is None

            if message.read_date:
                assert (
                    message.read_date.strftime("%d.%m.%Y")
                    == message_expected["DataPrzeczytania"]
                )
            else:
                assert message_expected["DataPrzeczytania"] is None
