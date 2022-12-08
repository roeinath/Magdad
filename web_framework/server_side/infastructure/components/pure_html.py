from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *


class PureHTML(UIComponent):
    def __init__(self, html_string="", style_classes=None):
        super().__init__()
        self.__html_string = html_string
        self.__style_classes = style_classes or {}

    def render(self):
        return {
            JSON_TYPE: JSON_PURE_HTML,
            JSON_ID: self.id,
            JSON_HTML_STRING: self.__html_string,
            JSON_STYLE_CLASSES: self.__style_classes
        }
