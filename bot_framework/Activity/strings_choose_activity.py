from typing import Callable, Dict
from fuzzywuzzy import process
from bot_framework.View.button_matrix_view import ButtonMatrixView
from bot_framework.View.view_container import ViewContainer
from bot_framework.session import Session
from bot_framework.Activity.activity import Activity
from APIs.Tools.ClosestStrings.closest_strings import get_closest_strings


class StringsChooseActivity(Activity):
    """
    Presents the user a list of buttons for choosing an amount of strings similar to an input string from
    a database of a lot of strings.
    """

    def __init__(self, view_container: ViewContainer,
                 all_options: [str],
                 submit_callback: Callable[[Session, list], None],
                 get_input_text: str = 'הקלד בחירות, מופרדות בפסיק:',
                 max_buttons: int = 6,
                 separator: str=','):
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
        self.separator = separator
        self.get_input_text = get_input_text
        self.submit_callback = submit_callback
        self.all_names = all_options
        self.max_buttons = max_buttons
        self.raw_object = None
        self.strings_chosen = []
        self.buttons = {}
        self.submit_buttons = [
            self.view_container.ui.create_button_view("אפס", self._reset),
            self.view_container.ui.create_button_view("הוסף עוד", self._continue),
            self.view_container.ui.create_button_view("סיים", self._submit)
        ]
        self.button_view: ButtonMatrixView = None
        self._reset(view_container.session, from_init=True)
        self.raw_object = self.button_view

    def draw(self):
        super().draw()


    def remove_raw(self):
        self.button_view.remove()

    def _get_button_matrix(self, inputs):
        matrix = []
        matches = []
        for key in inputs:
            new_matches = get_closest_strings(input=key, limit=max(1, int(self.max_buttons / len(inputs))), all_options=self.all_names)
            for match in new_matches:
                if not match in matches:
                    matches.append(match)

        template = '{color}\t{name}'
        color_map = {True: '\U0001F535', False: '\U0001F534'}
        self.buttons = {}
        for key in matches:
            self.buttons[key] = [False, self.view_container.ui.create_button_view(
                template.format(color=color_map[False], name=key), lambda s, k=key: self._click(s, k)
            )]
            matrix.append([self.buttons[key][1]])
        matrix.append(self.submit_buttons)
        return matrix

    def _click(self, session: Session, key: str):
        template = '{color}\t{name}'
        color_map = {True: '\U0001F535', False: '\U0001F534'}
        if self.buttons[key][0]:
            self.buttons[key][0] = False
        else:
            self.buttons[key][0] = True
        self.buttons[key][1] = self.view_container.ui.create_button_view(
            template.format(color=color_map[self.buttons[key][0]], name=key), lambda s, k=key: self._click(s, key)
        )
        matrix = []
        for button in self.buttons.values():
            matrix.append([button[1]])
        matrix.append(self.submit_buttons)
        self.button_view.update("סמן את האפשרויות המתאימות:", matrix)

    def _continue(self, session: Session):
        for key in self.buttons.keys():
            if self.buttons[key][0] and not key in self.strings_chosen:
                self.strings_chosen.append(key)
        self.view_container.ui.create_text_view(session, 'עד כה נבחרו: '+', '.join(self.strings_chosen)).draw()
        self.view_container.ui.create_text_view(session, self.get_input_text).draw()
        self.view_container.ui.get_text(session, self._got_input)

    def _submit(self, session: Session):
        for key in self.buttons.keys():
            if self.buttons[key][0] and not key in self.strings_chosen:
                self.strings_chosen.append(key)
        self.submit_callback(session, self.strings_chosen)

    def _reset(self, session: Session, from_init: bool = False):
        self.strings_chosen = []
        if not from_init:
            self.view_container.ui.create_text_view(session, 'הבחירות אופסו').draw()
        self.view_container.ui.create_text_view(session, self.get_input_text).draw()
        self.view_container.ui.get_text(session, self._got_input)


    def _got_input(self, session: Session, input: str):
        inputs = input.split(self.separator)
        self.button_view: ButtonMatrixView = self.view_container.ui.create_button_matrix_view(
            session,
            "סמן את האפשרויות הנכונות:",
            self._get_button_matrix(inputs)
        )
        self.button_view.draw()
