from typing import List, Callable

from bot_framework.Activity.FormActivity.Field.field import Field
from bot_framework.Activity.checkbox_activity import CheckBoxActivity
from bot_framework.View.view_container import ViewContainer


class CheckBoxField(Field[List[str]]):
    """
    Field that allows for multiple choice of str options.
    """

    def __init__(self, name: str, msg: str, options: List[str], value: List[str] = None):
        super().__init__(name, value)
        self.msg = msg
        self.options = options

    def show_input_view(self, view_container: ViewContainer, update_callback: Callable[[], None], hide_callback: Callable[[], None]):
        super().show_input_view(view_container, update_callback, hide_callback)

        checkbox = CheckBoxActivity(view_container, self.options, self.finish_input_view, max_buttons=len(self.options), title=self.msg)
        checkbox.draw()

    def human_readable_value(self):
        if self.value is None:
            return None

        new_value = ""

        for opt in self.value:
            new_value += str(opt) + ", "

        return new_value[:-2]
