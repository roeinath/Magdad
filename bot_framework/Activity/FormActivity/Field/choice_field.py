from typing import List, Callable, TypeVar, Generic, Dict

from bot_framework.Activity.FormActivity.Field.field import Field
from bot_framework.View.view_container import ViewContainer

T = TypeVar('T')


class ChoiceField(Field[T], Generic[T]):
    """
    Field that allows for single choice from list of objects.
    """

    def __init__(self, name: str, msg: str, options: Dict[T, str], value: T = None):
        super().__init__(name, value)
        self.msg = msg
        self.options = options

    def show_input_view(self, view_container: ViewContainer, update_callback: Callable[[], None], hide_callback: Callable[[], None]):
        super().show_input_view(view_container, update_callback, hide_callback)

        buttons = []

        for option_value, option_title in self.options.items():
            button = view_container.ui.create_button_view(option_title, lambda session, value=option_value: self.finish_input_view(session, value))
            buttons.append(button)

        view_container.ui.create_button_group_view(
            view_container.session,
            self.msg,
            buttons,
            view_container
        ).draw()

    def human_readable_value(self):
        if self.value is None:
            return None

        return self.options[self.value]
