from typing import Dict, TypeVar, Generic, Callable

from bot_framework.session import Session
from bot_framework.Activity.closest_name_activity import ClosestNameActivity
from bot_framework.Activity.FormActivity.Field.field import Field
from bot_framework.View.view_container import ViewContainer

T = TypeVar('T')


class ClosestNameField(Field[T], Generic[T]):
    """
    Field that allows the user to enter a string and
    presents the most similar objects to the string
    from an option list.
    """

    def __init__(self, name: str, input_msg: str, data: Dict[str, T], count: int, value: T = None):
        super().__init__(name, value)
        self.name = name
        self.input_msg = input_msg
        self.data = data
        self.count = count

        self.human_value = self._get_human_value(value)

    def show_input_view(self, view_container: ViewContainer, update_callback: Callable[[], None], hide_callback: Callable[[], None]):
        super().show_input_view(view_container, update_callback, hide_callback)

        view_container.ui.create_text_view(view_container.session, self.input_msg, view_container).draw()
        view_container.ui.get_text(view_container.session, lambda session, key: self.show_options(session, key, view_container))

    def show_options(self, session: Session, key: str, view_container: ViewContainer):
        activity = ClosestNameActivity(view_container, self.data, key, self.count, choose_callback=self.option_chosen, cancel=self.cancel_pressed)
        activity.draw()

    def option_chosen(self, session: Session, activity: ClosestNameActivity, value: str):
        self.human_value = self._get_human_value(value)
        activity.remove_raw()
        self.finish_input_view(session, value)

    def cancel_pressed(self, session: Session, activity: ClosestNameActivity):
        activity.remove_raw()
        self.cancel_input_view(session)

    def _get_human_value(self, value: T):
        if value is None:
            return None

        reversed_dict = dict(map(reversed, self.data.items()))

        return reversed_dict[value]

    def human_readable_value(self):
        if self.human_value is None:
            return None

        return self.human_value
