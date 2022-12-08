import math
from typing import Callable, Dict, List
from bot_framework.View.button_matrix_view import ButtonMatrixView
from bot_framework.View.view_container import ViewContainer
from bot_framework.session import Session
from bot_framework.Activity.activity import Activity
from bot_framework.ui.button import Button


class CheckBoxActivity(Activity):
    """
    Presents the user a list of buttons for choosing an amount of strings similar to an input string from
    a database of a lot of strings.
    """
    COLOR_MAP = {False: '⬜', True: '🔳'}
    SELECTED_MULT = '🔳'
    SELECTED_SINGL = '⬛️'
    SUBMIT_EMOJI = '✔️'

    def __init__(self, view_container: ViewContainer,
                 options: [str],
                 submit_callback: Callable[[Session, List[str]], None],
                 extra_callbacks: Dict[str, Callable[[Session, str], None]] = {},
                 title: str = 'בחר מהאפשרויות:',
                 max_buttons: int = 6,
                 max_selections: int = 0,
                 min_selections: int = 0,
                 simple_choice: bool = False):
        """
         Initializes a new CheckBoxActivity.
        :param ui: The UI to send through
        :param session: The Session to use (what user to send to?)
        :param options: All options the user can choose from.
        :param submit_callback: Function to be called when submitted
        :param extra_callbacks: Dict of submit name and functions, other than normal submit
                (for example - Cancel button)
        :param title: Text to appear above the checkbox buttons
        :param max_buttons: Amount of options to display, other options will be split into pages.
                Set to 0 to avoid paging.
        :param max_selections: Max number of selections
        :param min_selections: Min number of selections, under which the submit button won't appear
        :param simple_choice: Makes a single choice without selection, clicking on an answer immediately submits
        """
        super().__init__(view_container)

        self.page = 0
        self.raw_object = None
        self.answers: Dict[str, bool] = dict()
        self.buttons: Dict[str, Button] = dict()
        self.next_button = self.view_container.ui.create_button_view("▶️", self._next)
        self.prev_button = self.view_container.ui.create_button_view("◀️", self._prev)
        self.template = ''
        self.button_view: ButtonMatrixView = None
        self.title = ''
        self.select_stack: [str] = []
        self.submit_buttons: list = []

        self.submit_callback: Callable[[Session, str], None] = lambda a, b: ''
        self.extra_callbacks: Dict[str, Callable[[Session, str], None]] = {}
        self.max_buttons: int = 0
        self.options: [str] = []
        self.min_selections: int = 0
        self.max_selections: int = 0
        self.simple_choice: bool = None

        self._initiated = False
        self.drew = False
        self.update(view_container.session, options, submit_callback, extra_callbacks,
                    title, max_buttons, max_selections, min_selections,
                    simple_choice)
        self.raw_object = self.button_view

    def _get_title(self):
        title = self.title
        if not self.simple_choice:
            title += '\n\n' + 'נבחרו: ' + str(len(self.select_stack))
            if self.max_selections > 0:
                title += " מתוך " + str(self.max_selections)
        return title

    def update(self, session: Session, options: [str] = None,
               submit_callback: Callable[[Session, str], None] = None,
               extra_callbacks: Dict[str, Callable[[Session, str], None]] = None,
               title: str = None,
               max_buttons: int = None,
               max_selections: int = None,
               min_selections: int = None,
               simple_choice: bool = None,
               reset_answers: bool = True):
        """
        Updates the CheckBoxActivity.
        Unchanged parameters shouldn't be set.
        :param session: The Session to use (what user to send to?)
        :param options: All options the user can choose from.
        :param submit_callback: Function to be called when submitted
        :param extra_callbacks: Dict of submit name and functions, other than normal submit (for example - Cancel button)
        :param title: Text to appear above the checkbox buttons
        :param max_buttons: Amount of options to display, other options will be split into pages. Set to 0 to avoid paging.
        :param max_selections: Max number of selections
        :param min_selections: Min number of selections, under which the submit button won't appear
        :param simple_choice: Makes a single choice without selection, clicking on an answer immediately submits
        :param reset_answers: Determines whether selected checkboxes are deselected. Default is True.
        """

        if reset_answers:
            self.answers: Dict[str, bool] = dict()

        if options is not None:
            self.options = options
            for key in list(self.answers.keys()):
                if key not in options:
                    del self.answers[key]
            for option in options:
                if option not in self.answers.keys():
                    self.answers[option] = False

        if submit_callback is not None:
            self.submit_callback = submit_callback

        if extra_callbacks is not None:
            self.extra_callbacks = extra_callbacks

        if title is not None:
            self.title = title

        if submit_callback is not None or extra_callbacks is not None:
            self.submit_buttons = [
                self.view_container.ui.create_button_view(self.COLOR_MAP[False], self._reset)
            ]
            for text, callback in self.extra_callbacks.items():
                self.submit_buttons.append(
                    self.view_container.ui.create_button_view(text, lambda s, c=callback: self._submit(s, c))
                )
            self.submit_buttons.append(
                self.view_container.ui.create_button_view(self.SUBMIT_EMOJI, lambda s, c=self.submit_callback: self._submit(s, c)))

        if max_buttons is not None:
            self.max_buttons = max_buttons

        if max_selections is not None:
            self.max_selections = max_selections

        if min_selections is not None:
            self.min_selections = min_selections

        if simple_choice is not None:
            self.simple_choice = simple_choice
            self.template = '{name}' if simple_choice else '{color}\t{name}'


        if self.min_selections == 1 and self.max_selections == 1:
            self.COLOR_MAP[True] = self.SELECTED_SINGL
        else:
            self.COLOR_MAP[True] = self.SELECTED_MULT

        self._update_all_buttons()
        if self._initiated:
            self._update_view()
        else:
            self.button_view = self.view_container.ui.create_button_matrix_view(session, self._get_title(), self._get_button_matrix())
            self._initiated = True

    def draw(self):
        """
        Draws the activity. Can be drawn again after removed.
        """
        super().draw()
        self.button_view.draw()
        self.drew = True
        self._update_view()

    def remove_raw(self):
        self.button_view.remove()
        self.drew = False

    def _get_button_matrix(self):
        options = self.options
        add_navigate_buttons = False
        if 0 < self.max_buttons < len(options):
            options = options[self.page * self.max_buttons:]
            options = options[:self.max_buttons]
            add_navigate_buttons = True
        matrix = []

        for option in options:
            matrix.append([self.buttons[option]])
        if add_navigate_buttons and len(options) < self.max_buttons:
            empty_button = self.view_container.ui.create_button_view(' ', lambda s: '')
            for i in range(self.max_buttons - len(options)):
                matrix.append([empty_button])

        if add_navigate_buttons:
            matrix.append([])
            if self.page > 0:
                matrix[-1].append(self.prev_button)
            if self.page < -1 + math.ceil(len(self.options) / self.max_buttons):
                matrix[-1].append(self.next_button)

        if not self.simple_choice:
            if len(self.select_stack) >= self.min_selections:
                matrix.append(self.submit_buttons)
            else:
                matrix.append(self.submit_buttons[:-1])

        return matrix

    def _click(self, session: Session, key: str):
        if self.simple_choice:
            self.answers[key] = True
            self._submit(session, self.submit_callback)
            return

        self.answers[key] = not self.answers[key]

        if self.answers[key]:
            self.select_stack.append(key)
            if 0 < self.max_selections < len(self.select_stack):
                dumped_key = self.select_stack[0]
                self.answers[dumped_key] = False
                self.buttons[dumped_key] = self.ui.create_button_view(
                    self.template.format(color=self.COLOR_MAP[False], name=dumped_key),
                    lambda s, k=dumped_key: self._click(s, k)
                )
                self.select_stack = self.select_stack[1:]
        elif key in self.select_stack:
            i = self.select_stack.index(key)
            self.select_stack = self.select_stack[:i] + self.select_stack[i + 1:]

        self.buttons[key] = self.view_container.ui.create_button_view(
            self.template.format(color=self.COLOR_MAP[self.answers[key]], name=key), lambda s, k=key: self._click(s, k)
        )

        self._update_view()

    def get_answer(self) -> [str]:
        answer: [str] = []
        for option in self.options:
            if self.answers[option]:
                answer.append(option)
        return answer

    def _submit(self, session: Session, callback: Callable[[Session, list], None]):
        self.remove()
        callback(session, self.get_answer())

    def _next(self, session: Session):
        if self.page < -1 + math.ceil(len(self.options) / self.max_buttons):
            self.page += 1
            self._update_view()

    def _prev(self, session: Session):
        if self.page > 0:
            self.page -= 1
            self._update_view()

    def _update_all_buttons(self):
        self.buttons = {}
        for option in self.options:
            self.buttons[option] = self.view_container.ui.create_button_view(
                self.template.format(color=self.COLOR_MAP[self.answers[option]], name=option),
                lambda s, k=option: self._click(s, k)
            )

    def _update_view(self):
        if self.drew:
            try:
                self.button_view.update(self._get_title(), self._get_button_matrix())
            except Exception as e:
                print(e)
                pass

    def _reset(self, session: Session, from_init: bool = False):
        for option in self.options:
            self.answers[option] = False
        self.select_stack = []
        self._update_all_buttons()
        if not from_init:
            self._update_view()
