from web_framework.server_side.infastructure import request_handlers
import web_framework.server_side.infastructure.ids_manager as ids_manager
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *
from typing import Callable, List


class UploadFiles(UIComponent):
    def __init__(self, upload_action: Callable = None, files: List = None):
        super().__init__()
        if upload_action:
            func_id = ids_manager.gen_action_id(lambda json: upload_action(json['files']))
            self.__action = self.method_to_url(func_id)
        else:
            self.__action = None
        self.__files = files or []

    def get_files(self):
        return self.__files

    def add_file(self, file):
        self.__files.append(file)
        self.update_files(self.__files)

    def update_files(self, files):
        self.__files = files
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_ID: self.id, JSON_FILES: self.__files}
        })

    def render(self):
        return {
            JSON_TYPE: JSON_UPLOAD,
            JSON_ACTION: self.__action,
            JSON_ID: self.id,
            JSON_FILES: self.__files
        }
