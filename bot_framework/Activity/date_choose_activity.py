from __future__ import annotations
from typing import Callable
from datetime import date, datetime
import calendar

from bot_framework.View.button_matrix_view import ButtonMatrixView
from bot_framework.View.view_container import ViewContainer
from bot_framework.session import Session
from bot_framework.Activity.activity import Activity
from bot_framework.ui.button import Button
from dateutil.relativedelta import relativedelta


class DateChooseView(Activity):
    """
    Presents the user a Calendar which he can
    choose a date from. Asks the feature
    for a choose_callback, which notifies the feature
    once a date is chosen, and includes this view, the relevent Session
    and the chosen date. This View will NOT be closed automatically, you
    will have to close it yourself.
    """

    HEBREW_SHORT_DAYS = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ש']
    CANCEL_CHOOSE_DATE = "ביטול"
    NO_DAY_BUTTON_TEXT = " "

    def __init__(self, view_container: ViewContainer, choose_callback: Callable[[DateChooseView, Session, date], None],
                 chosen_date: date = None, title: str = "בחר תאריך"):
        """
        Initializes a new DateChooseView.
        :param ui: The UI to send throught
        :param session: The Session to use (what user to send to?)
        :param choose_callback: Choose callback to notify once a date was chosen
        :param chosen_date: Allows to set a default chosen date
        """
        super().__init__(view_container)

        self.choose_callback = choose_callback
        self.chosen_date = chosen_date
        self.view_month_start = self._get_month_start(chosen_date)
        self.title = title

        self.button_view: ButtonMatrixView = self.view_container.ui.create_button_matrix_view(
            view_container.session,
            self._get_text_status(),
            self._get_button_matrix()
        )

    def draw(self):
        super().draw()

        self.button_view.draw()
        self.raw_object = self.button_view

    def update(self, chosen_date: date):
        """
        Updates this View to show a calendar including the given
        new date, and to choose it.
        :param chosen_date: The date to update to
        :return:
        """
        super().update()

        if chosen_date == self.chosen_date:
            raise Exception("Cant update a view with the same details.")

        self.chosen_date = chosen_date
        self.view_month_start = self._get_month_start(chosen_date)

        self.button_view.update(
            self._get_text_status(),
            self._get_button_matrix()
        )

    def remove_raw(self):
        self.button_view.remove()

    def _next_month_clicked(self, session: Session):
        self.view_month_start += relativedelta(months=1)

        self.button_view.update(
            self._get_text_status(),
            self._get_button_matrix()
        )

    def _prev_month_clicked(self, session: Session):
        self.view_month_start -= relativedelta(months=1)

        self.button_view.update(
            self._get_text_status(),
            self._get_button_matrix()
        )

    def _date_clicked(self, session: Session, chosen_date: date):
        self.update(chosen_date)

        self.choose_callback(self, session, chosen_date)

    def _get_month_start(self, date: date) -> date:
        if date is None:
            #  Return the current month's start
            return datetime.now().date().replace(day=1)

        #  Calculate the date's month start
        return date.replace(day=1)

    def _get_text_status(self) -> str:
        return self.title

    def _get_button_matrix(self):
        matrix = []

        IGNORE = lambda ses: None
        now = datetime.now().date()
        month = self.view_month_start.month
        year = self.view_month_start.year

        # First row - Month and Year
        matrix += [[
            Button(calendar.month_name[self.view_month_start.month] + " " + str(self.view_month_start.year), IGNORE)
        ]]

        # Second row - Week Days
        calendar.setfirstweekday(6)
        matrix += [list(map(
            lambda x: Button(x, IGNORE),
            [calendar.day_abbr[6]] + calendar.day_abbr[0:6]
        ))]

        #  The calendar
        my_calendar = calendar.monthcalendar(year, month)
        for week in my_calendar:
            row = []
            for day in week:
                if day == 0:
                    row.append(Button(DateChooseView.NO_DAY_BUTTON_TEXT, IGNORE))
                    continue

                day_to_print = str(day)
                selected_date = date(year, month, day)

                #  Special emoji for today
                if selected_date == now:
                    # print a sum emoji
                    day_to_print = "\u2600"

                #  Special for the selected date
                if selected_date == self.chosen_date:
                    day_to_print = "*" + day_to_print + "*"

                row.append(Button(
                    day_to_print,
                    lambda session, selected_date=selected_date: self._date_clicked(session, selected_date)
                ))

            matrix += [row]

        # Last row - Actions
        matrix += [[
            Button("<", self._prev_month_clicked),
            Button(DateChooseView.CANCEL_CHOOSE_DATE, IGNORE),
            Button(">", self._next_month_clicked)
        ]]

        return matrix
