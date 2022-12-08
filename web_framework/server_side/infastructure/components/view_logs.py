from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent


class ViewLogs(UIComponent):
    def __init__(self, path: str):
        super().__init__()
        self.__path = path

    def render(self):
        return {
            JSON_TYPE: 'ViewLogs',
            JSON_ID: self.id,
            JSON_PATH: self.__path
        }
