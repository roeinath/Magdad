from __future__ import annotations
from bot_framework.View.view import View
from bot_framework.View.view_container import ViewContainer


class ButtonMatrixView(View):
    """
    Creates a matrix of buttons, by the given button array.
    each button contains It's title and a function to call, once
    the button is pressed.
    """

    def __init__(self, view_container: ViewContainer, text: str = "", buttons = None):
        """
        Creates a new ButtonMatrixView
        :param ui: The UI to draw with
        :param session: The session to draw at (what user to send to?)
        :param text: The text to show above the buttons
        :param buttons: A matrix of buttons to send
        """
        super().__init__(view_container)
        self.text = text
        self.buttons = buttons if buttons else [[]]

    def update(self, new_text: str, new_buttons):
        """
        Updates the current ButtonMatrixView with new data.
        :param new_text: New text to show above the buttons.
        :param new_buttons: New button matrix
        :return:
        """
        super().update()

        self.text = new_text
        self.buttons = new_buttons if new_buttons else [[]]

    def remove_raw(self):
        pass

    def __eq__(self, other: ButtonMatrixView):
        """Overrides the default implementation"""
        if isinstance(other, ButtonMatrixView):
            return self.text == other.text and\
                   self.buttons == other.buttons

        return False
