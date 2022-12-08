import telegram

from bot_framework.View.button_group_view import ButtonGroupView
from bot_framework.Telegram.View.telegram_view_container import TelegramViewContainer


class TelegramButtonGroupView(ButtonGroupView):

    def __init__(self, view_container: TelegramViewContainer, text: str = "", buttons = None):
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

    def update(self, new_text: str, new_buttons=None):
        super().update(new_text, new_buttons)

        # Create the button markup
        markup = self._get_current_markup()

        #  Update the message
        message = self.raw_object.result()

        if message is not None:
            message.edit_text(self.text, reply_markup=markup)

    def _get_current_markup(self):
        keyboard_buttons = []
        for b in self.buttons:
            button_id = self.get_session().id + ";" + self.get_session().add_button(b)
            keyboard_buttons.append([telegram.InlineKeyboardButton(text=b.title, callback_data=button_id)])

        # Generate the keyboard markup and prepare the message it will be sent with.
        keyboard = keyboard_buttons
        markup = telegram.InlineKeyboardMarkup(keyboard)

        return markup

    def remove_raw(self):
        if self.raw_object.result() is not None:
            self.raw_object.result().delete()
