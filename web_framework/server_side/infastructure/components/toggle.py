import web_framework.server_side.infastructure.ids_manager as ids_manager
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *
from typing import Callable



class Toggle(UIComponent):
    def __init__(self, action: Callable = None, initial_state=True, on_label='on', off_label='off',
                 bg_color='none', fg_color='none', size=SIZE_MEDIUM):
        super().__init__(bg_color=bg_color, fg_color=fg_color, size=size)
        if action:
            func_id = ids_manager.gen_action_id(lambda _: action())
            self.__action = self.method_to_url(func_id)
        else:
            self.__action = None
        self.__initial_state = initial_state
        self.__on_label = on_label
        self.__off_label = off_label

    def set_action(self, action):
        if action:
            func_id = ids_manager.gen_action_id(lambda _: action())
            self.__action = self.method_to_url(func_id)
        else:
            self.__action = None

    def render(self):
        return {
            JSON_TYPE: JSON_BUTTON,
            JSON_ID: self.id,
            JSON_ACTION: self.__action,
            JSON_SIZE: self.size,
            JSON_INITIAL_STATE: self.__initial_state,
            JSON_ON_LABEL: self.__on_label,
            JSON_OFF_LABEL: self.__off_label
        }
