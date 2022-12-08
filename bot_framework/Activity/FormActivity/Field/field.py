from typing import Callable, TypeVar, Generic, Optional

from bot_framework.session import Session
from bot_framework.View.view_container import ViewContainer


T = TypeVar('T')


class Field(Generic[T]):
    """
    The field class represents a general
    field in the FormActivity, that allows the
    user to interact with the form, and change data.
    This class is generic for the type of the value it holds.
    A field input view is started using show_input_view()
    and the interaction is ended via cancel_input_view() when
    the value is not changed, or when the value is changed
    using finish_input_view()
    """

    def __init__(self, name: str, value: T = None):
        """
        Initializes the form
        :param name: The name of the field to be displayed in the FormActivity
        :param value: The initial value of the field, shown to the user
        via the ```human_readable_value()``` function.
        """
        self.value: T = value
        self.name: str = name

        self.update_callback = None
        self.hide_callback = None

    def human_readable_value(self) -> Optional[str]:
        """
        Returns an human readable representation of the value, to be
        shown in the form next to the field name.
        """

        if self.value is None:
            return None

        return str(self.value)

    def show_input_view(self, view_container: ViewContainer, update_callback: Callable[[], None], hide_callback: Callable[[], None]):
        """
        Shows the view that allows the user to enter the
        input for this form, for changing the value.
        :param view_container: The ViewContainer the field can draw in
        :param update_callback: To call when the value is changed
        :param hide_callback: To call when the input view needs to be hidden/finished.
        :return:
        """
        self.update_callback = update_callback
        self.hide_callback = hide_callback

    def cancel_input_view(self, session: Session):
        """
        Cancels the input view, and hides it.
        :param session:
        :return:
        """
        self._hide_input_view()

    def finish_input_view(self, session: Session, new_value: T):
        """
        Finished the input view, updates the FormActivity
        and hides it.
        :param session:
        :param new_value: New chosen value for the field.
        :return:
        """
        self.value = new_value
        self.update_callback()
        self._hide_input_view()

    def _hide_input_view(self):
        """
        Hides the input view.
        :return:
        """
        self.hide_callback()

        self.hide_callback = None
        self.update_callback = None
