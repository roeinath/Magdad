from web_framework.server_side.infastructure import request_handlers
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent


class TextField(UIComponent):
    def __init__(self, placeholder="", bg_color="none", fg_color="black",
                 bold: bool = False, italic: bool = False):
        """
        TextField component
        :param placeholder: text to display when empty
        :param bg_color: background color
        :param fg_color: text color
        :param bold: bold or not
        :param italic: italic or not
        """
        super().__init__(text=placeholder, bg_color=bg_color, fg_color=fg_color)
        self.__bold = bold
        self.__italic = italic

    def render(self):
        return {
            JSON_TYPE: JSON_TEXT_FIELD,
            JSON_ID: self.id,
            JSON_TEXT: self.text,
            JSON_BG_COLOR: self.bg_color,
            JSON_FG_COLOR: self.fg_color,
            JSON_BOLD: self.__bold,
            JSON_ITALIC: self.__italic
        }

    def update_text(self, text: str, bold: bool = False, italic: bool = False):
        """
        Updates the text field's placeholder
        :param text: new text
        :param bold: bold or not
        :param italic: italic or not
        :return:
        """
        self.text = text
        self.__bold = bold
        self.__italic = italic
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_ID: self.id,
                         JSON_TEXT: self.text,
                         JSON_BOLD: self.__bold,
                         JSON_ITALIC: self.__italic}
        })

    def update_placeholder(self, placeholder, bold=False, italic=False):
        """
        Updates the text field's placeholder
        :param text: new text
        :param bold: bold or not
        :param italic: italic or not
        :return:
        """
        self.update_text(placeholder, bold, italic)
