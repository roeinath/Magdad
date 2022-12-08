import telegram

from bot_framework.Telegram.View.telegram_view_container import TelegramViewContainer
from bot_framework.View.text_view import TextView
import telegram


class TelegramTextView(TextView):

    def __init__(self, view_container: TelegramViewContainer, text: str = ""):
        # adding a \n and blank emoji in the end of the text
        # this is because telegram adds the time in the last line it sometimes overrides the text
        super().__init__(view_container, text)

    def draw(self):
        super().draw()
        # Get the chat id of the session (which is unique for a user)
        chat_id = self.get_session().user.telegram_id

        #  Add empty last line to prevent design problem
        text = self.text + "\n" + "󠀠 "

        # Send the message using the raw_bot reference to the chat id from the session.
        raw_msg = self.view_container.ui.raw_bot.send_message(self.get_session(), chat_id, text, parse_mode=telegram.ParseMode.MARKDOWN,
                                               disable_web_page_preview=True)

        # Add it to the session.
        self.raw_object = raw_msg
        self.raw_object = raw_msg

    def update(self, text):
        super().update(text)

        #  Add empty last line to prevent design problem
        text = self.text + "\n" + "󠀠 "

        #  Update the object
        self.raw_object.result().edit_text(text)

    def remove_raw(self):
        if self.raw_object.result() is not None:
            self.raw_object.result().delete()
