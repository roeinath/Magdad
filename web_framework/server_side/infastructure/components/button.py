from typing import Callable

import web_framework.server_side.infastructure.ids_manager as ids_manager
import web_framework.server_side.infastructure.request_handlers as request_handlers
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *


class Button(UIComponent):
    def __init__(self, text="", action: Callable = None, bg_color="#2e7ea6", fg_color='none', size=SIZE_MEDIUM,
                 font=None):
        super().__init__(text=text, bg_color=bg_color, fg_color=fg_color, size=size)
        if action:
            func_id = ids_manager.gen_action_id(lambda _: action())
            self.__action = self.method_to_url(func_id)
        else:
            self.__action = None
        self.__font = font

    def set_action(self, action):
        if action:
            func_id = ids_manager.gen_action_id(lambda _: action())
            self.__action = self.method_to_url(func_id)
        else:
            self.__action = None

    def render(self):
        return {JSON_TYPE: JSON_BUTTON,
                JSON_ID: self.id,
                JSON_TEXT: self.text,
                JSON_ACTION: self.__action,
                JSON_SIZE: self.size,
                JSON_BG_COLOR: self.bg_color,
                JSON_FG_COLOR: self.fg_color,
                JSON_FONT: self.__font
                }
