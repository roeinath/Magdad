from typing import Callable

from web_framework.server_side.infastructure.components.stack_panel import StackPanel, HORIZONTAL
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.pop_up import PopUp

CONFIRMATION_TEXT = "האם את/ה בטוח/ה?"


class ConfirmationButton(UIComponent):

    def __init__(self, text="", action: Callable = None, bg_color="#2e7ea6", fg_color='none', size=SIZE_MEDIUM,
                 font=None, confirmation_text=CONFIRMATION_TEXT):
        super().__init__()
        self.__confirmation_text = confirmation_text
        self.__action = action

        self.__main_stack = StackPanel([])
        self.__popup = self.__set_popup()
        self.__button = Button(text, self.__popup.show, bg_color, fg_color, size, font)

        self.__main_stack.add_component(self.__button)
        self.__main_stack.add_component(self.__popup)

    def __set_popup(self):
        buttons_stack = StackPanel([Button("ביטול", bg_color='red', action=self.__hide_popup),
                                    Button("אישור", action=self.__do_action)], orientation=HORIZONTAL)
        return PopUp(buttons_stack, title=self.__confirmation_text, is_shown=False, is_cancelable=False)

    def __hide_popup(self):
        self.__popup.hide()


    def __do_action(self):
        self.__hide_popup()
        self.__action()

    def set_action(self, action):
        self.__button.set_action(action)

    def render(self):
        return self.__main_stack.render()
