import telegram

from bot_framework.Telegram.View.telegram_view_container import TelegramViewContainer
from bot_framework.View.button_matrix_view import ButtonMatrixView


class TelegramButtonMatrixView(ButtonMatrixView):
    """
    Telegram implementation of @TalpiBotAPI.View.button_matrix_view.ButtonMatrixView
    """
    def __init__(self, view_container: TelegramViewContainer, text: str = "", buttons = None):
        """
        Creates a new ButtonMatrixView
        :param ui: The UI to draw with
        :param session: The session to draw at (what user to send to?)
        :param text: The text to show above the buttons
        :param buttons: A matrix of buttons to send
        """
        super().__init__(view_container, text, buttons)

        self.view_container = view_container

    def draw(self):
        super().draw()

        # Get the chat to send to
        chat_id = self.get_session().user.telegram_id

        # Create the button markup
        markup = self._get_current_markup()

        # Send the message
        self.raw_object = self.view_container.ui.raw_bot.send_message(
            self.get_session(), chat_id, self.text, reply_markup=markup
        )

    def update(self, new_text: str, new_buttons = None):
        super().update(new_text, new_buttons)

        # Create the button markup
        markup = self._get_current_markup()

        #  Update the message
        message = self.raw_object.result()

        if message is not None:
            message.edit_text(self.text, reply_markup=markup)

    def _get_current_markup(self) -> telegram.InlineKeyboardMarkup:
        keyboard_buttons = []
        for row in self.buttons:
            row_buttons = []
            if type(row) != list:
                row = [row]
            for b in row:
                button_id = self.get_session().id + ";" + self.get_session().add_button(b)
                row_buttons.append(telegram.InlineKeyboardButton(text=b.title, callback_data=button_id))

            keyboard_buttons.append(row_buttons)

        # Generate the keyboard markup and prepare the message it will be sent with.
        keyboard = keyboard_buttons
        markup = telegram.InlineKeyboardMarkup(keyboard)

        return markup

    def remove_raw(self):
        if self.raw_object.result() is not None:
            self.raw_object.result().delete()
