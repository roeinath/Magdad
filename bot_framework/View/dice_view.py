from __future__ import annotations
from bot_framework.View.view import View
from bot_framework.View.view_container import ViewContainer


class DiceView(View):
    def __init__(self, view_container: ViewContainer):
        super().__init__(view_container)
        self.raw_object = None

    def update(self, text):
        super().update()

    def remove_raw(self):
        pass

    def __eq__(self, other: DiceView):
        """Overrides the default implementation"""
        if isinstance(other, DiceView):
            return True

        return False
