from typing import Optional
from bot_framework.Telegram.telegram_bot_manager_webhook import BotWebhookSettings
from APIs import settings as APIs_settings
import os
"""
setting.py - a settings file for the system. The TalpiBotSettings is a singleton class.

In order to get the settings in your code you can use TalpiBotSettings.get()

For example:
    return TalpiBotSetting.get().database_creds.username

DO NOT UPLOAD YOUR SETTINGS FILE TO GIT.
"""


def use_web_hooks() -> Optional[BotWebhookSettings]:
    if 'CONTAINER_NAME' in os.environ:
        # TODO: delete this
        return BotWebhookSettings(
            port=8080,
            ssl_private_key='/bot/ssl/server.key',
            ssl_server_certificate='/bot/ssl/cert.pem',
            base_url='https://talpibot.westeurope.cloudapp.azure.com:8443/'
        )
    return None



def load_settings():
    APIs_settings.load_settings()
