import telegram

from bot_framework.Telegram.View.telegram_view_container import TelegramViewContainer
from bot_framework.View.dice_view import DiceView
import telegram


class TelegramDiceView(DiceView):

    def __init__(self, view_container: TelegramViewContainer):
        super().__init__(view_container)

        self.view_container = view_container

    def draw(self):
        super().draw()
        # Get the chat id of the session (which is unique for a user)
        chat_id = self.get_session().user.telegram_id

        raw_bot: telegram.bot.Bot = self.view_container.ui.raw_bot
        raw_dice_message = raw_bot.send_dice(chat_id)

        self.raw_object = raw_dice_message

    def update(self, text):
        super().update(text)
        raise NotImplementedError()

    def remove_raw(self):
        pass
