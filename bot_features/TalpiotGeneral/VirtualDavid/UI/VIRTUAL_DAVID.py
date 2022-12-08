from bot_framework import *
from APIs.ExternalAPIs import *
from APIs.TalpiotAPIs import *
from APIs.Database import *
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.ui import UI, Button
from APIs.TalpiotAPIs.User.user import User
import os
import pathlib


class VirtualDavid(BotFeature):

    HOME = pathlib.Path(__file__).resolve().parent.parent / "Static/וירטואל דוד"

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)

    def main(self, session: Session):
        self.manager(session, self.HOME)

    def manager(self, session: Session, path: pathlib.Path):
        self.ui.clear(session)
        msg = None
        buttons = []
        files = os.listdir(path)
        for f in files:
            if f == "info.txt":
                with open(path / "info.txt", "r") as info:
                    msg = info.read()
            else:
                buttons.append(self.ui.create_button_view(f, lambda s, ff=f: self.manager(s, path / ff)))
        if path != self.HOME:
            buttons.append(self.ui.create_button_view("חזרה", lambda s: self.manager(s, path.parent)))
        else:
            buttons.append(self.ui.create_button_view("יציאה", lambda s: self.ui.summarize_and_close(s)))
        if msg and buttons:
            self.ui.create_button_group_view(session, msg, buttons).draw()
        elif msg:
            self.ui.create_text_view(session, msg).draw()
        elif buttons:
            self.ui.create_button_group_view(session, "בחר את הקטגוריה שאתה מעוניין בה", buttons).draw()

    def is_authorized(self, user: User) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        return "מתלם" in user.role
