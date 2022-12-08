from __future__ import annotations
from typing import Callable

from bot_framework.Activity.FormActivity.Field.field import Field
from bot_framework.View.button_matrix_view import ButtonMatrixView
from bot_framework.View.view_container import ViewContainer
from bot_framework.session import Session
from bot_framework.Activity.activity import Activity


class FormActivity(Activity):
    """
    Presents the user a list of buttons for choosing an amount of strings similar to an input string from
    a database of a lot of strings.
    """

    EMPTY_ANSWER = "הכנס תשובה"
    SEND_FORM = "שלח טופס"

    class ValidationException(Exception):
        def __init__(self, message: str):
            self.message = message

    def __init__(self, view_container: ViewContainer, formObject, name: str, callback: Callable[[Session, FormActivity, object], None]):
        """
        Initializes a new DateChooseView.
        :param ui: The UI to send through
        :param session: The Session to use (what user to send to?)
        """
        super().__init__(view_container)
        self.inner_view_container = ViewContainer(self.view_container.session, self.view_container.ui)
        self.formObject = formObject
        self.form_name = name
        self.form = None
        self.callback = callback
        self.buttons_grid = []
        self.error_shown = False

    def draw(self):
        """
        Draws the FormActivity on the screen.
        :return:
        """
        super().draw()

        #  Create all the fields
        count = 0
        for field_name, field in self.formObject.__dict__.items():
            #  Generate the row of the field: One cell with the name,
            #  and second cell with the value.
            #  on click on one of the fields will trigger the callback
            #  that shows the input view of the field.
            show_input_callback = self._generate_show_input_view_callback(field, count)

            #  Get the human readable value, if it exists
            title = field.human_readable_value()
            if title is None:
                title = FormActivity.EMPTY_ANSWER

            #  Generate the row
            buttons = [
                self.view_container.ui.create_button_view(title, show_input_callback),
                self.view_container.ui.create_button_view(field.name, show_input_callback)
            ]

            self.buttons_grid.append(buttons)
            count += 1

        #  Create the "SEND" button
        send_button = self.view_container.ui.create_button_view(FormActivity.SEND_FORM, self.finish_button_clicked)
        self.buttons_grid.append([send_button])

        #  Show the form
        self.form: ButtonMatrixView = self.view_container.ui.create_button_matrix_view(
            self.view_container.session,
            self.form_name,
            self.buttons_grid,
            self.inner_view_container
        )

        self.form.draw()

    def show_error(self, error: str):
        """
        Shows an error on the form main message.
        :param error: The error to show
        :return:
        """

        self.form.update("%s\n*שגיאה:*\n%s" % (self.form_name, error), self.buttons_grid)
        self.error_shown = True

    def hide_error(self):
        """
        Removes the error from the form main message.
        :return:
        """

        if not self.error_shown:
            return

        self.form.update(self.form_name, self.buttons_grid)
        self.error_shown = False

    def get_values(self):
        return self.formObject

    def _generate_show_input_view_callback(self, field: Field, index: int):
        """
        Generates the callbacks needed for: Clicking on field and showing input view,
        updating the form once a value is updated, and hiding the input view on
        demand.
        :param field: The field to generate for
        :param index: The index of the field in the form's table
        :return: callback for clicking on the field.
        """
        view_container: ViewContainer = ViewContainer(self.view_container.session, self.view_container.ui)

        def update_callback():
            self._update(index, field.human_readable_value())

        def hide_callback():
            self.hide_error()
            view_container.remove()
            self.view_container.views.remove(view_container)

        def show_callback(session: Session):
            field.show_input_view(view_container, update_callback, hide_callback)
            self.view_container.views.append(view_container)

        return show_callback

    def _update(self, index: int, new_value: str):
        """
        Updates the value of a specific field
        in the form's table
        :param index: the index of the field
        :param new_value: New value for the field
        :return:
        """
        super().update()

        self.buttons_grid[index][0].title = new_value
        self.form.update(self.form_name, self.buttons_grid)

    def finish_button_clicked(self, session: Session):
        """
        Called when the form's "finish" button is clicked.
        this function wakes the given callback to the form,
        informing the feature that was using the form, the user
        wants to finish the form.
        :param session: The session of the user calling this.
        :return:
        """

        try:
            return self.callback(self.view_container.session, self, self.get_values())
        except FormActivity.ValidationException as e:
            self.show_error(e.message)

    def remove_raw(self):
        """
        Removes this activity from the screen.
        :return:
        """
        self.inner_view_container.remove()
