import urllib.parse
from typing import Callable

import web_framework.server_side.infastructure.ids_manager as ids_manager
from APIs.TalpiotAPIs.Gitlab.gitlab_file_tree import GitlabFileTree
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent


class FileTree(UIComponent):
    def __init__(self, action: Callable = None, size=SIZE_MEDIUM, start_folder = 'bot_features', branch = 'development'):
        super().__init__(size=size)
        self.__action = None
        self.set_action(action)
        self.__files = GitlabFileTree.objects(name=start_folder, branch = branch).first()
        self.__files = self.__files.to_json() if self.__files is not None else {}

    def set_action(self, action: Callable):
        if action:
            func_id = ids_manager.gen_action_id(lambda json: action(json['url']))
            self.__action = self.method_to_url(func_id)

    def render(self):
        return {
            JSON_TYPE: 'FileTree',
            JSON_ID: self.id,
            JSON_ACTION: self.__action,
            JSON_SIZE: self.size,
            JSON_FILES: self.__files
        }
