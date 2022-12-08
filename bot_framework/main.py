import bot_framework.configuration_setup as ConfigSetup
import bot_framework.settings as settings
from APIs.TalpiotAPIs import User
from APIs.TalpiotSystem import TalpiotSettings
from bot_framework.Telegram.telegram_bot_manager import TelegramBotManager
from bot_framework.Telegram.telegram_bot_manager_webhook import TelegramBotManagerWebhook
from bot_framework.bot_manager import BotManager


def get_bot_manager() -> BotManager:
    bot_token = TalpiotSettings.get().bot_token
    print(bot_token)
    if settings.use_web_hooks() is not None:
        return TelegramBotManagerWebhook(bot_token, settings.use_web_hooks(), User)

    return TelegramBotManager(bot_token, User)


def main():
    ConfigSetup.run_setup()

    bm: BotManager = get_bot_manager()
    bm.run()


if __name__ == '__main__':
    main()
