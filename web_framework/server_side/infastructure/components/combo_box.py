from web_framework.server_side.infastructure.ui_component import UIComponent
import web_framework.server_side.infastructure.ids_manager as ids_manager

from typing import Callable, Dict
from web_framework.server_side.infastructure.constants import *


class ComboBox(UIComponent):
    def __init__(self, options: Dict[str, str], on_changed: Callable[[str], None], default_value: str = None):
        super().__init__()
        self.__options = options
        self.__selected = None

        def on_changed_wrapper(json):
            if 'chosen' in json:
                on_changed(json['chosen'])

        if on_changed:
            func_id = ids_manager.gen_action_id(lambda json: on_changed_wrapper(json))
            self.__on_changed = self.method_to_url(func_id)
        else:
            self.__on_changed = None

        self.__default_value = default_value

    def render(self):
        return {JSON_TYPE: 'ComboBox',
                JSON_ID: self.id,
                JSON_OPTIONS: self.__options,
                JSON_ACTION: self.__on_changed,
                JSON_DEFAULT_VALUE: self.__default_value
                }

    def set_selected_option(self, option):
        self.add_action({
            JSON_ACTION: 'set_selected_option',
            JSON_VALUE: {
                JSON_ID: self.id,
                'selected_option': option,
            }
        })
