from __future__ import annotations
from typing import Callable, Dict, Optional
from fuzzywuzzy import process
from bot_framework.View.button_matrix_view import ButtonMatrixView
from bot_framework.View.view_container import ViewContainer
from bot_framework.session import Session
from bot_framework.Activity.activity import Activity
from APIs.Tools.ClosestStrings.closest_strings import get_closest_strings


class ClosestNameActivity(Activity):
    """ivi
    Presents the user a list of buttons for choosing an amount of strings similar to an input string from
    a database of a lot of strings.
    """

    def __init__(self, view_container: ViewContainer, data: Dict[str, object], key: str, count: int, choose_callback: Callable[[Session, ClosestNameActivity, object], None], try_again: Optional[Callable[[Session], None]] = None, cancel: Optional[Callable[[Session, ClosestNameActivity], None]] = None):
        """
        Initializes a new DateChooseView.
        :param ui: The UI to send through
        :param session: The Session to use (what user to send to?)
        :param choose_callback: Choose callback to notify once a date was chosen
        :param data: Map from objects to the strings that describe them. On choose_callback, an object from data.keys() will be returned.
        :param key: The key string to search in data.values()
        :param count: the amount of objects to display to the user
        """
        super().__init__(view_container)

        self.choose_callback = choose_callback
        self.data = data
        self.key = key
        self.count = count
        self.raw_object = None
        self.try_again = try_again
        self.cancel = cancel

        self.button_view: ButtonMatrixView = self.view_container.ui.create_button_matrix_view(
            view_container.session,
            "בחר באפשרות שאתה מחפש:",
            self._get_button_matrix()
        )

    def draw(self):
        super().draw()

        self.button_view.draw()
        self.raw_object = self.button_view

    def remove_raw(self):
        self.button_view.remove()

    def _get_button_matrix(self):
        matrix = []

        options_fuzz = process.extractBests(self.key, self.data.keys(), limit=self.count)
        matches = [x for (x, y) in options_fuzz]

        matches = get_closest_strings(input=self.key, limit=self.count, all_options=self.data.keys())

        for key in matches:
            matrix.append([self.view_container.ui.create_button_view(key, lambda s, k=key: self.choose_callback(s, self, self.data[k]))])

        if self.try_again is not None:
            matrix.append([self.view_container.ui.create_button_view("נסה שנית", self.try_again)])

        if self.cancel is not None:
            matrix.append([self.view_container.ui.create_button_view("בטל", lambda s: self.cancel(s, self))])

        return matrix
