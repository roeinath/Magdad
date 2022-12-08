from __future__ import annotations
import typing
from typing import List

from bot_framework.View.drawable import Drawable

if typing.TYPE_CHECKING:
    from bot_framework import Session, UI


class ViewContainer(Drawable):
    def __init__(self, session: Session, ui: UI):
        self.views: List[Drawable] = []
        self.session: Session = session
        self.ui = ui

    def draw(self):
        pass

    def remove(self):
        view_list = self.views[:]
        if len(view_list) == 0:
            return

        for view in view_list:
            view.remove()

        self.views = []
