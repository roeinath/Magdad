from typing import Callable

from APIs.TalpiotAPIs.TalpiShared.talpishared_object import TalpiSharedObject
from web_framework.server_side.infastructure import request_handlers
import web_framework.server_side.infastructure.ids_manager as ids_manager
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *
from APIs.ExternalAPIs.GoogleDrive.file_to_upload import FileToUpload


class DisplayFile(UIComponent):
    def __init__(self, file: FileToUpload = None, action: Callable = None):
        super().__init__()
        self.__file: FileToUpload = file
        self.__talpishared_object = None
        if action:
            func_id = ids_manager.gen_action_id(lambda _: action())
            self.__action = self.method_to_url(func_id)
            self.__file.url = None
        else:
            self.__action = None

    def get_file(self):
        return self.__file

    def update_file(self, file: FileToUpload):
        self.__file = file
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_ID: self.id,
                         JSON_FILE_TYPE: self.__file.type,
                         JSON_FILE_NAME: self.__file.name,
                         JSON_FILE_SIZE: self.__file.size,
                         JSON_FILE_LAST_MODIFIED: self.__file.last_modified
                         }
        })

    def update_file_url(self, url: str):
        self.__file.url = url
        self.update_file(self.__file)

    def set_action(self, action):
        if action:
            func_id = ids_manager.gen_action_id(lambda _: action())
            self.__action = self.method_to_url(func_id)
        else:
            self.__action = None

    def add_uri(self, uri):
        self.add_action({
            JSON_ACTION: JSON_REDIRECT,
            JSON_VALUE: {
                JSON_ID: self.id,
                JSON_URL: uri,
            }
        })

    @staticmethod
    def from_talpishared_object(talpishared_object: TalpiSharedObject, action: Callable = None, url: str = None):
        file_type = talpishared_object.name.rsplit(".")[-1] if talpishared_object.children is None else 'folder'
        file_to_upload = FileToUpload(talpishared_object.name, file_type, url=url)
        display_file = DisplayFile(file_to_upload, action)
        display_file.__talpishared_object = talpishared_object
        return display_file

    def render(self):
        return {
            JSON_TYPE: JSON_DISPLAY_FILE,
            JSON_ID: self.id,
            JSON_FILE_TYPE: self.__file.type,
            JSON_FILE_NAME: self.__file.name,
            JSON_FILE_SIZE: self.__file.size,
            JSON_FILE_LAST_MODIFIED: self.__file.last_modified,
            JSON_URL: self.__file.url,
            JSON_ACTION: self.__action
        }
