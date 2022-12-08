from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent


class Label(UIComponent):
    def __init__(self, text="", bg_color="none", fg_color="black",
                 bold: bool = False, italic: bool = False, size=SIZE_MEDIUM, width="auto"):
        """
            TextField component
            :param text: text to display
            :param bg_color: background color
            :param fg_color: text color
            :param bold: bold or not
            :param italic: italic or not
        """
        super().__init__(text=text, bg_color=bg_color, fg_color=fg_color, size=size)
        self.__bold = bold
        self.__italic = italic
        self.__width = width

    def render(self):
        return {
            JSON_TYPE: JSON_LABEL,
            JSON_ID: self.id,
            JSON_TEXT: self.text,
            JSON_BG_COLOR: self.bg_color,
            JSON_FG_COLOR: self.fg_color,
            JSON_SIZE: self.size,
            JSON_BOLD: self.__bold,
            JSON_ITALIC: self.__italic,
            JSON_WIDTH: self.__width
        }

    def update_text(self, text, bold=None, italic=None, size=None):
        """
        Updates the label's text
        :param text: new text
        :param bold: bold or not
        :param italic: italic or not
        :return:
        """
        self.text = text
        if bold != None:
            self.__bold = bold
        if italic != None:
            self.__italic = italic
        if size != None:
            self.size = size
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_ID: self.id,
                         JSON_TEXT: self.text,
                         JSON_BOLD: self.__bold,
                         JSON_ITALIC: self.__italic,
                         JSON_SIZE: self.size}
        })
