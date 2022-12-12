from abc import ABC, abstractmethod
import inspect
from typing import ClassVar

import web_framework.server_side.infastructure.ids_manager as ids_manager
from web_framework.server_side.infastructure import request_handlers
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page


class UIComponent(ABC):
    def __init__(self, text='', fg_color=JSON_NONE, bg_color=None, size=SIZE_SMALL, relative_width=None):
        """
        The component constructor
        :param text: component text
        :param fg_color: text color
        :param bg_color: background color
        """
        self.id = ids_manager.gen_component_id(self)
        self.text = text
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.size = size
        self.relative_width = relative_width
        self.session_id = None
        # self.session_id = inspect.currentframe().f_back.f_back.f_locals['self'].session_id

    def get_panret_page(self):
        curr = inspect.currentframe()
        while curr is not Page:
            curr = curr.f_back
        return curr.f_locals['self']

    @abstractmethod
    def render(self) -> None:
        """
        Add an 'add component' action for this component to the action list
        """
        pass

    def method_to_url(self, method_id):
        return f'/run_func/?method_id={method_id}'

    def submit_to_url(self, method_id):
        return f'/get_data/?method_id={method_id}'

    def update_color(self, bg_color: str = None, fg_color: str = None):
        """
        change component bg color and fg color
        :param bg_color:
        :param fg_color:
        :return:
        """
        self.fg_color = fg_color if fg_color is not None else self.fg_color
        self.bg_color = bg_color if bg_color is not None else self.bg_color
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_ID: self.id,
                         JSON_BG_COLOR: self.bg_color,
                         JSON_FG_COLOR: self.fg_color}
        })

    def update_text(self, text: str):
        """
        update component text
        :param text:
        :return:
        """
        self.text = text
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_ID: self.id,
                         JSON_TEXT: self.text}
        })

    def redirect_page(self, new_url: str, override: bool = False):
        """
        Redirects the page to a new url
        :param new_url: the full or partial url to redirect to
        :param override: if True, the url will be replaced in the browser's history (default is False)
        :return: noting
        """
        self.add_action({
            JSON_ACTION: JSON_REDIRECT,
            JSON_VALUE: {JSON_ID: self.id, JSON_URL: new_url, JSON_OVERRIDE: override}
        })

    def add_action(self, action):
        request_handlers.actions_lsts[self.session_id].append(action)

    def get_first_level_children(self):
        return []

    def set_session_id(self, session_id):
        self.session_id = session_id
        for child in self.get_first_level_children():
            child.set_session_id(session_id)