from typing import Callable
from datetime import datetime

from bot_framework.Activity.time_choose_activity import TimeChooseView
from bot_framework.session import Session
from bot_framework.Activity.FormActivity.Field.field import Field
from bot_framework.View.view_container import ViewContainer


class TimeField(Field[datetime]):
    """
    Field that allows the user to enter a time
    """

    def __init__(self, name: str, msg: str, value: datetime = None):
        super().__init__(name, value)
        self.msg = msg

    def show_input_view(self, view_container: ViewContainer, update_callback: Callable[[], None], hide_callback: Callable[[], None]):
        super().show_input_view(view_container, update_callback, hide_callback)

        view_container.ui.create_text_view(view_container.session, self.msg, view_container).draw()
        timeChoose = TimeChooseView(view_container, self.time_choose_finished)
        timeChoose.draw()

    def time_choose_finished(self, activity: TimeChooseView, session: Session, value: datetime):
        activity.remove_raw()
        self.finish_input_view(session, value)

    def human_readable_value(self):
        if self.value is None:
            return None

        return self.value.strftime("%H:%M")
