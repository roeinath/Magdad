from typing import Dict, TypeVar, Generic, Callable

from bot_framework.Activity.names_choose_activity import NamesChooseActivity
from bot_framework.session import Session
from bot_framework.Activity.FormActivity.Field.field import Field
from bot_framework.View.view_container import ViewContainer

T = TypeVar('T')


class NamesChooseField(Field[T], Generic[T]):
    """
    Field that allows the user to enter a string and
    presents the most similar objects to the string
    from an option list.
    Allows choice of multiple values.
    """

    def __init__(self, name: str, input_msg: str, data: Dict[str, T], count: int, value: [T] = None):
        super().__init__(name, value)
        self.name = name
        self.input_msg = input_msg
        self.data = data
        self.count = count

        self.human_value = self._get_human_value(value)

    def show_input_view(self, view_container: ViewContainer, update_callback: Callable[[], None], hide_callback: Callable[[], None]):
        super().show_input_view(view_container, update_callback, hide_callback)

        view_container.ui.create_text_view(view_container.session, self.input_msg, view_container).draw()
        self.show_options(view_container.session, view_container)

    def show_options(self, session: Session, view_container: ViewContainer):
        activity = NamesChooseActivity(
            view_container,
            submit_callback=self.option_chosen,
            from_names=self.data.keys(),
            max_buttons=self.count
        )

        activity.draw()

    def option_chosen(self, session: Session, value: [str]):
        #  Transform value into Objects
        value = [self.data[x] for x in value]

        self.human_value = self._get_human_value(value)
        self.finish_input_view(session, value)

    def cancel_pressed(self, session: Session, activity: NamesChooseActivity):
        activity.remove_raw()
        self.cancel_input_view(session)

    def _get_human_value(self, value: [T]):
        if value is None:
            return None

        reversed_dict = dict(map(reversed, self.data.items()))

        return ", ".join(list(map(lambda x: reversed_dict[x], value)))

    def human_readable_value(self):
        if self.human_value is None:
            return None

        return self.human_value
