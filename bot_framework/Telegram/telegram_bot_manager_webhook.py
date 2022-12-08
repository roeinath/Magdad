from typing import Type

from bot_framework.Telegram.telegram_bot_manager import TelegramBotManager
from bot_framework.bot_logger import BotLogger
from bot_framework.bot_user import BotUser
from bot_framework.Commands.bot_command_handler import BotCommandHandler


class BotWebhookSettings:
    def __init__(self, port, ssl_private_key, ssl_server_certificate, base_url):
        self.port = port
        self.ssl_private_key = ssl_private_key
        self.ssl_server_certificate = ssl_server_certificate
        self.base_url = base_url


class TelegramBotManagerWebhook(TelegramBotManager):
    def __init__(self, token: str, webhook_settings: BotWebhookSettings, user_type: Type[BotUser]):
        super().__init__(token, user_type)

        self.webhook_settings = webhook_settings

    def run(self):
        # Start the Bot - Register webhook at telegram
        self.updater.start_webhook(listen='0.0.0.0',
                                   port=self.webhook_settings.port,
                                   url_path=self.token,
                                   key=self.webhook_settings.ssl_private_key,
                                   cert=self.webhook_settings.ssl_server_certificate,
                                   webhook_url=self.webhook_settings.base_url + self.token)

        BotCommandHandler(self.ui)

        BotLogger.success("Bot started running.")
        BotLogger.success("You can now open telegram and use it (webhook).")

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()
