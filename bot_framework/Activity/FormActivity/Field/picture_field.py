from typing import Callable
from telegram import File
from bot_framework.Activity.FormActivity.Field.field import Field
from bot_framework.View.view_container import ViewContainer


class PictureField(Field[File]):
    """
    Field that allows the user to upload an image.
    """

    PICTURE_VALID = "תמונה נקלטה"

    def __init__(self, name: str, msg: str, value: File = None):
        super().__init__(name, value)
        self.msg = msg

    def show_input_view(self, view_container: ViewContainer, update_callback: Callable[[], None], hide_callback: Callable[[], None]):
        super().show_input_view(view_container, update_callback, hide_callback)

        view_container.ui.create_text_view(view_container.session, self.msg, view_container).draw()
        view_container.ui.get_photo(view_container.session, self.finish_input_view)

    def human_readable_value(self):
        if self.value is None:
            return None

        return PictureField.PICTURE_VALID
