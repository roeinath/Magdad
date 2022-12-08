from typing import Callable, Dict
from fuzzywuzzy import process
from bot_framework.View.button_matrix_view import ButtonMatrixView
from bot_framework.View.view_container import ViewContainer
from bot_framework.session import Session
from bot_framework.Activity.activity import Activity
from bot_framework.Activity.strings_choose_activity import StringsChooseActivity


class NamesChooseActivity(Activity):
    """
    Presents the user a list of buttons for choosing an amount of strings similar to an input string from
    a database of a lot of strings.
    """

    def __init__(self, view_container: ViewContainer,
                 submit_callback: Callable[[Session, list], None],
                 from_names: [str] = None,
                 max_buttons: int = 8):
        """
        Initializes a new DateChooseView.
        :param ui: The UI to send through
        :param session: The Session to use (what user to send to?)
        :param choose_callback: Choose callback to notify once a date was chosen
        :param data: Map from objects to the strings that describe them. On choose_callback, an object from data.keys() will be returned.
        :param key: The key string to search in data.values()
        :param count: the amount of suggestions for each name
        """
        super().__init__(view_container)

        self.activity = StringsChooseActivity(view_container, from_names,
                                              submit_callback,
                                              max_buttons=max_buttons,
                                              get_input_text='הקלד שמות מופרדים בפסיק:')

    def draw(self):
        super().draw()
        self.activity.draw()

    def remove_raw(self):
        self.activity.remove_raw()
