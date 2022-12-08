from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class BotUser(ABC):
    @property
    @abstractmethod
    def telegram_id(self) -> int:
        pass

    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @staticmethod
    def get_by_telegram_id(telegram_id: int) -> Optional[BotUser]:
        pass
