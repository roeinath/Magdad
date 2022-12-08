from __future__ import annotations
from typing import Dict, Callable, TYPE_CHECKING

from bot_framework.ui.button import Button

if TYPE_CHECKING:
    from bot_framework.ui.ui import UI
from bot_framework.View.view_container import ViewContainer

from bot_framework.bot_user import BotUser
from APIs.TalpiotAPIs import SecretCodeManager

"""
A session represents an interaction between the user and a feature.
"""


class Session:
    id_num: str = "0"
    sessions: Dict[str, Dict[str, Session]] = {}

    def __init__(self, feature_name: str, user: BotUser, ui: UI):
        """
        Create a new session
        :param feature_name: the name of the feature this session belongs to
        :param user: the user this session is applied to
        """
        # if user is None:
        #     raise Exception("ERROR- USER IS NONE IN SESSION CREATION")

        self.user: BotUser = user
        self.data: Dict = dict()
        self.id: str = Session.generate_id()
        self.view_container: ViewContainer = ViewContainer(self, ui)
        self.buttons: Dict[str, Button] = {}
        self.next_id: str = "0"
        self.feature_name = feature_name
        self.active = True  # Will be false when the session is closed, in which case views will not be appended.

        if user is not None:
            Session.register_session(self)

    def add_button(self, button: Button) -> str:
        """
        Add a button callback to the session
        :param func: the callback of the button
        :return: the id assigned to the button in this session
        """
        button_id = self.next_id
        self.next_id = str(int(self.next_id) + 1)

        button_id = Session.gen_random_id_token() + button_id

        self.buttons[str(button_id)] = button

        return button_id

    @staticmethod
    def generate_id() -> str:
        """
        Get the next id for a session
        :return:
        """
        # Session.id_num = str(int(Session.id_num) + 1)
        Session.id_num = Session.gen_random_id_token()# + Session.id_num
        return Session.id_num

    @staticmethod
    def register_session(session: Session):
        """
        Registers a session object into
        :param session:
        :return:
        """
        user = session.user

        #  If there is no dictionary for user.id
        #  we should create it
        if user.id not in Session.sessions:
            Session.sessions[user.id] = {}

        #  Add it.
        Session.sessions[user.id][session.id] = session

    @staticmethod
    def delete_session(session: Session):
        """
        # todo this is not correct
        Registers a session object into
        :param session:
        :return:
        """
        user = session.user

        del session.buttons
        session.buttons = {}

        if user.id not in Session.sessions:
            Session.sessions[user.id] = {}

        del Session.sessions[user.id][session.id]

    @staticmethod
    def gen_random_id_token():
        return SecretCodeManager.generate_code()
