from __future__ import annotations
from typing import Dict
from bot_framework.bot_user import BotUser


class TestBotUser(BotUser):
    get_dictionary: Dict[int, TestBotUser] = dict()

    def __init__(self, telegram_id, id):
        self._telegram_id = telegram_id
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def telegram_id(self):
        return self._telegram_id

    @staticmethod
    def get_by_telegram_id(telegram_id: int):
        return TestBotUser.get_dictionary[telegram_id]
