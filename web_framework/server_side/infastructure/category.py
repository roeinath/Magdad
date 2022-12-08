from abc import ABC, abstractmethod
from typing import List

from APIs.TalpiotAPIs import User


class Category(ABC):
    def __init__(self, pages: dict):
        self.pages = pages

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def is_authorized(self, user: User):
        return True
