from typing import Callable

import web_framework.server_side.infastructure.ids_manager as ids_manager
import web_framework.server_side.infastructure.request_handlers as request_handlers
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *


class LogViewer(UIComponent):
    def __init__(self, file_path: str, do_update: bool = True):
        super().__init__()
        self.file_path: str = file_path

        func_id = ids_manager.gen_action_id(lambda json: self.log_update(json['current_position']))
        self.__action = None
        if do_update:
            self.__action = self.method_to_url(func_id)

    def log_update(self, current_position):
        print("called log_update", current_position)

        log_file = open(self.file_path, "r")
        log_file.seek(current_position)
        added_text = log_file.read()
        new_position = log_file.tell()

        added_text = '\n'.join(reversed(added_text.split('\n')))
        if added_text:
            self.add_action({
                JSON_ACTION: JSON_add_component,
                JSON_VALUE: {
                    JSON_ID: self.id,
                    JSON_CHILD: {
                        "component": {'id': None, 'type': None},
                        JSON_TEXT: added_text,
                        JSON_POSITION: new_position
                    }
                }
            })

    def render(self):
        return {
            JSON_TYPE: 'LogViewer',
            JSON_ID: self.id,
            JSON_ACTION: self.__action,
        }
