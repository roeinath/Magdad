from __future__ import annotations
from bot_framework.View.view import View
from bot_framework.View.view_container import ViewContainer


class ButtonGroupView(View):

    def __init__(self, view_container: ViewContainer, text: str = "", buttons = None):
        super().__init__(view_container)
        self.text = text
        self.buttons = buttons if buttons else []

    def update(self, new_text: str, new_buttons):
        super().update()
        check = True
        for i in range(len(self.buttons)):
            if self.buttons[i].title != new_buttons[i].title:
                check = False
                break
        if new_text == self.text and self.buttons == new_buttons and check:
            raise Exception("Cant update a view with the same details.")

        self.text = new_text
        self.buttons = new_buttons if new_buttons else []

    def remove_raw(self):
        pass

    def __eq__(self, other: ButtonGroupView):
        """Overrides the default implementation"""
        if isinstance(other, ButtonGroupView):
            return self.text == other.text and\
                   self.buttons == other.buttons

        return False
