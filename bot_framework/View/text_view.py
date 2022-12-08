from __future__ import annotations
from bot_framework.View.view import View
from bot_framework.View.view_container import ViewContainer


class TextView(View):
    def __init__(self, view_container: ViewContainer, text: str = ""):
        super().__init__(view_container)
        self.text = text
        self.raw_object = None

    def update(self, text):
        super().update()

        if text == self.text:
            raise Exception("Cant update a view with the same details.")

        self.text = text

    def remove_raw(self):
        pass

    def __eq__(self, other: TextView):
        """Overrides the default implementation"""
        if isinstance(other, TextView):
            return self.text == other.text

        return False
