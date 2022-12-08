import math
from typing import Callable, Dict
from fuzzywuzzy import process
from bot_framework.View.button_matrix_view import ButtonMatrixView
from bot_framework.View.view_container import ViewContainer
from bot_framework.session import Session
from bot_framework.Activity.activity import Activity
from APIs.Tools.ClosestStrings.closest_strings import get_closest_strings
from bot_framework.View.view import View


class LibraryActivity(Activity):
    """
    Presents the user a list of buttons for choosing an amount of strings similar to an input string from
    a database of a lot of strings.
    """

    def __init__(self, view_container: ViewContainer,
                 data_dict: dict, title: str = "בחר שאלה או קטגוריה:", max_buttons=8):
        """
        Initializes a new DateChooseView.
        :param ui: The UI to send through
        :param session: The Session to use (what user to send to?)
        :param data_dict: Dict containing all data of the library
        :param title: Text to be displayed before button selection
        :param max_buttons: Max number of buttons of categories \ questions to display. More buttons than that,
                            the library will add next and previous navigation buttons.
        """
        super().__init__(view_container)
        self.title = title
        self.qna_dict = data_dict
        self.max_questions = max_buttons
        self.page = 0
        self.raw_object = None
        self.stack = []
        self.in_answer = False
        self.submit_buttons = [

        ]
        self.close_button = self.view_container.ui.create_button_view("❌", self._close)
        self.back_button = self.view_container.ui.create_button_view("🔙", self._back)
        self.next_button = self.view_container.ui.create_button_view("▶️", self._next)
        self.prev_button = self.view_container.ui.create_button_view("◀️", self._prev)

        self.button_view: ButtonMatrixView = None
        self.raw_object = self.button_view
        self._update_buttons(session=view_container.session)

    def draw(self):
        super().draw()

    def remove_raw(self):
        self.button_view.remove()

    def _get_curr_dict(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        else:
            return self.qna_dict

    def _update_buttons(self, session=None):
        curr_dict = self._get_curr_dict()
        keys = list(curr_dict.keys())
        add_navigate_buttons = False
        if (self.max_questions > 0 and len(keys) > self.max_questions):
            keys = keys[self.page * self.max_questions:]
            keys = keys[:self.max_questions]
            add_navigate_buttons = True
        matrix = []
        for key in keys:
            matrix.append([
                self.view_container.ui.create_button_view(key, lambda s, k=key: self._click(s, k))
            ])
        if (add_navigate_buttons):
            matrix.append([])
            if self.page > 0:
                matrix[-1].append(self.prev_button)
            if self.page < -1 + math.ceil(len(list(self._get_curr_dict().keys())) / self.max_questions):
                matrix[-1].append(self.next_button)
        title = self.title
        matrix.append([])
        if len(self.stack) > 0:
            matrix[-1].append(self.back_button)
        matrix[-1].append(self.close_button)

        if self.button_view == None:
            self.button_view = self.view_container.ui.create_button_matrix_view(session, self.title, matrix)
            self.button_view.draw()
        else:
            if(self.in_answer):
                self.button_view = self.view_container.ui.create_button_matrix_view(session, 'לחץ לחזרה:', [self.back_button])
                self.button_view.draw()
            else:
                self.button_view.update(self.title, matrix)

    def _click(self, session: Session, key: str):
        curr_dict = self._get_curr_dict()
        to_draw = curr_dict[key]
        if type(to_draw) == dict:
            self.stack.append(curr_dict[key])
            self._update_buttons()
            return
        self.button_view.remove()
        if type(to_draw) == list:
            for item in to_draw:
                self._draw_item(session, item)
        else:
            self._draw_item(session, to_draw)
        self.in_answer = True
        self._update_buttons(session=session)

    def _draw_item(self, session, item):
        if type(item) == str:
            item = self.view_container.ui.create_text_view(session, item)
        print(type(item))
        if issubclass(type(item), View):
            view: View = item
            view.remove()
            view.draw()

    def _back(self, session: Session):
        if self.in_answer:
            self.in_answer = False
        else:
            self.stack = self.stack[:-1]
            self.page = 0
        self._update_buttons()

    def _next(self, session: Session):
        if self.page < -1 + math.ceil(len(list(self._get_curr_dict().keys())) / self.max_questions):
            self.page += 1
            self._update_buttons()

    def _prev(self, session: Session):
        if self.page > 0:
            self.page -= 1
            self._update_buttons()

    def _close(self, session: Session):
        self.ui.summarize_and_close(session,[])
