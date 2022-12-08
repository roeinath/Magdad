from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure import ids_manager

PYTHON = 'python'
DRACULA = 'dracula'


class CodeEditor(UIComponent):
    def __init__(self, text: str = "", language: str = PYTHON, theme: str = DRACULA, editable=True,
                 width="70vw", height="60vh"):
        super().__init__(text)
        self.__theme = theme
        self.__language = language
        self.__editable = editable
        self.__width = width
        self.__height = height

        func_id = ids_manager.gen_action_id(self.__update_code)
        self.__action = self.submit_to_url(func_id)

    def render(self):
        return {
            JSON_TYPE: 'CodeEditor',
            JSON_ID: self.id,
            JSON_TEXT: self.text,
            JSON_LANGUAGE: self.__language,
            JSON_THEME: self.__theme,
            JSON_EDITABLE: self.__editable,
            JSON_WIDTH: self.__width,
            JSON_HEIGHT: self.__height,
            JSON_ACTION: self.__action
        }

    def __update_code(self, text):
        self.text = text

    def update_code(self, text):
        self.__update_code(text)
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {
                JSON_ID: self.id,
                JSON_TEXT: self.text
            }
        })

    def get_code(self):
        return self.text
