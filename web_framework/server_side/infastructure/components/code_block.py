from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent

PYTHON = 'python'


class CodeBlock(UIComponent):
    def __init__(self, text: str = "", language: str = PYTHON, highlight_lines: list = None, is_copyable=True,
                 width=None, height=None):
        super().__init__(text)
        self.language = language
        self.highlight_lines = highlight_lines
        self.is_copyable = is_copyable
        self.__width = width
        self.__height = height

    def render(self):
        return {
            JSON_TYPE: 'CodeBlock',
            JSON_ID: self.id,
            JSON_TEXT: self.text,
            JSON_LANGUAGE: self.language,
            JSON_HIGHLIGHT_LINES: self.highlight_lines,
            JSON_IS_COPYABLE: self.is_copyable,
            JSON_HEIGHT: self.__height,
            JSON_WIDTH: self.__width,
        }

    def update_code(self, text):
        self.text = text

    def get_code(self):
        return self.text
