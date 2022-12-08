import uuid
from abc import ABC, abstractmethod
from typing import List

from APIs.TalpiotAPIs import User
from web_framework.server_side.infastructure import request_handlers
from web_framework.server_side.infastructure.constants import *

class Page(ABC):
    def __init__(self, params={}):
        self.__components: List = []
        self.__components_ids: List[str] = []

    @abstractmethod
    def get_page_ui(self, user: User):
        """
        This method returns the root UIComponent of the page.
        """
        pass

    @staticmethod
    def get_title() -> str:
        """
        returns the title of the page
        :return: str - title of page
        """
        pass

    def get_initial_ui(self, user):
        ui = self.get_page_ui(user)

        return ui

    @staticmethod
    def is_authorized(user: User):
        return MATLAM in user.role  # Only the people of the base
