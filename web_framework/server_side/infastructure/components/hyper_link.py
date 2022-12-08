from web_framework.server_side.infastructure import request_handlers
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent


class HyperLink(UIComponent):
    def __init__(self, text="", bg_color="none", fg_color="black",
                 bold: bool = False, italic: bool = False, size=SIZE_MEDIUM, width="auto", url="."):
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
        self.__url = url

    def render(self):
        return {
            JSON_TYPE: JSON_HYPERLINK,
            JSON_ID: self.id,
            JSON_TEXT: self.text,
            JSON_BG_COLOR: self.bg_color,
            JSON_FG_COLOR: self.fg_color,
            JSON_SIZE: self.size,
            JSON_BOLD: self.__bold,
            JSON_ITALIC: self.__italic,
            JSON_WIDTH: self.__width,
            JSON_URL: self.__url,
        }

    def update_text(self, text):
        """
        Updates the link's text
        :param text: new text
        :return:
        """
        self.text = text
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_ID: self.id,
                         JSON_TEXT: self.text,
                         JSON_BOLD: self.__bold,
                         JSON_ITALIC: self.__italic,
                         JSON_SIZE: self.size,
                         JSON_URL: self.__url}
        })

    def update_url(self, url):
        """
        Updates the link's text
        :param url:
        :param text: new text
        :return:
        """
        self.__url = url
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_ID: self.id,
                         JSON_TEXT: self.text,
                         JSON_BOLD: self.__bold,
                         JSON_ITALIC: self.__italic,
                         JSON_SIZE: self.size,
                         JSON_URL: self.__url}
        })
