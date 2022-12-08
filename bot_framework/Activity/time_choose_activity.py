from __future__ import annotations
from typing import Callable
from datetime import datetime

from bot_framework.View.button_matrix_view import ButtonMatrixView
from bot_framework.View.view_container import ViewContainer
from bot_framework.session import Session
from bot_framework.Activity.activity import Activity
from bot_framework.ui.button import Button
from bot_framework.ui.ignored_button import IgnoredButton


class TimeChooseView(Activity):
    """
    Presents the user a Calendar which he can
    choose a date from. Asks the feature
    for a choose_callback, which notifies the feature
    once a date is chosen, and includes this view, the relevent Session
    and the chosen date. This View will NOT be closed automatically, you
    will have to close it yourself.
    """

    TIME_CHOOSE = "הקלד זמן"
    TIME_CHOSEN = "נבחר הזמן"
    TIME_TEMPLATE = "%s%s:%s%s"
    EMPTY_BUTTON_TEXT = " "
    EMPTY_CHAR = "X"
    SAVE = "שמור"
    EDIT = "ערוך"
    NOT_RIGHT_TIME_ERROR = "שגיאה פורמט זמן לא תקין"

    def __init__(self, view_container: ViewContainer, choose_callback: Callable[[TimeChooseView, Session, datetime], None], chosen_time: datetime = None):
        """
        Initializes a new DateChooseView.
        :param ui: The UI to send throught
        :param session: The Session to use (what user to send to?)
        :param choose_callback: Choose callback to notify once a date was chosen
        :param chosen_time: Allows to set a default chosen date
        """
        super().__init__(view_container)

        self.choose_callback = choose_callback
        self.chosen_time = chosen_time
        self._current_time: list = self._generate_current_time(chosen_time)

        self.sub_container = ViewContainer(view_container.session, view_container.ui)

        self.button_view: ButtonMatrixView = self.view_container.ui.create_button_matrix_view(
            view_container.session,
            self._get_text_status(),
            self._get_button_matrix(),
            view_container=self.sub_container
        )


    def draw(self):
        super().draw()

        self.button_view.draw()
        self.raw_object = self.button_view

    def update(self, chosen_time: datetime):
        """
        Updates this View to show a calendar including the given
        new date, and to choose it.
        :param chosen_time: The time to update to
        :return:
        """
        super().update()

        if chosen_time == self.chosen_time:
            raise Exception("Cant update a view with the same details.")

        self.chosen_time = chosen_time
        self._current_time = self._generate_current_time(chosen_time)

        self.button_view.update(
            self._get_text_status(),
            self._get_button_matrix()
        )

    def remove_raw(self):
        self.button_view.remove()

    def _get_text_status(self) -> str:
        title = TimeChooseView.TIME_CHOOSE

        if self.chosen_time is not None:
            title = TimeChooseView.TIME_CHOSEN

        return title \
               + ":\n" \
               + TimeChooseView.TIME_TEMPLATE % self._add_padding_to_time()

    def _add_padding_to_time(self) -> tuple:
        array = list(self._current_time)

        if len(array) < 4:
            array += [TimeChooseView.EMPTY_CHAR] * (4-len(array))

        return tuple(array)

    def _generate_current_time(self, time: datetime = None) -> [str]:
        if time is None:
            return []

        return self._split_into_two_dec(time.hour) + self._split_into_two_dec(time.minute)

    def _split_into_two_dec(self, num: int) -> [str]:
        """
        Splits a number into array of 2 smallest decimals.
        :param num: int
        :return: array of two decimals
        """

        return [(int(num/10))%10] + [num%10]

    def _add_digit(self, session: Session, digit: int):
        if len(self._current_time) >= 4:
            return

        self._current_time.append(digit)

        self.button_view.update(
            self._get_text_status(),
            self._get_button_matrix()
        )

    def _remove_digit(self, session: Session):
        if len(self._current_time) == 0:
            return

        self._current_time.pop()

        self.button_view.update(
            self._get_text_status(),
            self._get_button_matrix()
        )

    def _get_current_hour_and_minute(self) -> tuple:
        if len(self._current_time) != 4:
            return (-1, -1)

        h = 10 * self._current_time[0] + self._current_time[1]
        m = 10 * self._current_time[2] + self._current_time[3]

        return (h, m)

    def _save(self, session: Session):
        h, m = self._get_current_hour_and_minute()

        if h == -1 or h < 0 or h >= 60 or m < 0 or m >= 60:
            self.button_view.update(
                self._get_text_status() + "\n" + TimeChooseView.NOT_RIGHT_TIME_ERROR,
                self._get_button_matrix()
            )
            return

        self.chosen_time = datetime.now()
        self.chosen_time = self.chosen_time.replace(hour=h, minute=m)

        self.button_view.update(
            self._get_text_status(),
            self._get_button_matrix()
        )

        self.choose_callback(self, session, self.chosen_time)

    def _edit(self, session: Session):
        if self.chosen_time is None:
            return

        self._current_time = self._generate_current_time(self.chosen_time)
        self.chosen_time = None

        self.button_view.update(
            self._get_text_status(),
            self._get_button_matrix()
        )

    def _get_button_matrix(self) -> [[Button]]:
        matrix: [[Button]] = []

        if self.chosen_time is not None:
            matrix += [[
                Button(TimeChooseView.EDIT, self._edit)
            ]]

            return matrix

        #  Create button pad
        matrix += [[
            Button("1", self._add_digit, 1),
            Button("2", self._add_digit, 2),
            Button("3", self._add_digit, 3),
        ]]

        matrix += [[
            Button("4", self._add_digit, 4),
            Button("5", self._add_digit, 5),
            Button("6", self._add_digit, 6),
        ]]

        matrix += [[
            Button("7", self._add_digit, 7),
            Button("8", self._add_digit, 8),
            Button("9", self._add_digit, 9),
        ]]

        matrix += [[
            Button("DEL", self._remove_digit),
            Button("0", self._add_digit, 0),
            IgnoredButton(TimeChooseView.EMPTY_BUTTON_TEXT),
        ]]

        #  Able to save
        if self._get_current_hour_and_minute() != (-1, -1):
            matrix += [[
                Button(TimeChooseView.SAVE, self._save)
            ]]

        return matrix
