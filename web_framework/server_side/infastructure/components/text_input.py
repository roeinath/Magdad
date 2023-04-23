from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure import ids_manager


class TextInput(UIComponent):
    def __init__(self, text="", text_holder="", bg_color="none", fg_color="black",
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
        self.__text_holder = text_holder

        func_id = ids_manager.gen_action_id(self.__update_text)
        self.__action = self.submit_to_url(func_id)

    def render(self):
        return {
            JSON_TYPE: 'TextInput',
            JSON_ID: self.id,
            JSON_TEXT: self.__text_holder,
            JSON_BG_COLOR: self.bg_color,
            JSON_FG_COLOR: self.fg_color,
            JSON_SIZE: self.size,
            JSON_BOLD: self.__bold,
            JSON_ITALIC: self.__italic,
            JSON_WIDTH: self.__width,
            JSON_ACTION: self.__action
        }

    def __update_text(self, text):
        self.text = text

    def update_text(self, text):
        self.__update_text(text)
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {
                JSON_ID: self.id,
                JSON_TEXT: self.text
            }
        })

    def get_text(self):
        return self.text
