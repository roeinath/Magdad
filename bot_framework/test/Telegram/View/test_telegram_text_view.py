import unittest
from unittest.mock import MagicMock

from bot_framework.session import Session
from bot_framework.Telegram.telegram_ui import TelegramUI
from bot_framework.Telegram.View.telegram_text_view import TelegramTextView
from bot_framework.test.mock_container import MockContainer
from bot_framework.test.test_bot_user import TestBotUser



class TestTelegramTextView(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        bot = MockContainer()
        bot.send_photo = MagicMock()
        bot.send_message = MagicMock()
        bot.send_contact = MagicMock()

        dispatcher = MockContainer()
        dispatcher.add_handler = MagicMock()

        cls.ui = TelegramUI(bot, dispatcher, TestBotUser)
        cls.user = TestBotUser(telegram_id='id_test', id="123")
        cls.session = cls.ui.create_session("Testing", cls.user)

    def test_draw(self):
        view = TelegramTextView(self.session.view_container, "test")
        view.draw()
        args, kwargs = self.ui.raw_bot.send_message.call_args
        self.assertEqual(args[0], self.session)
        self.assertEqual(args[1], self.user.telegram_id)
        self.assertEqual(args[2], "test\n\U000e0020 ")

    def test_update(self):
        view = TelegramTextView(self.session.view_container, "test")
        view.draw()
        view.raw_object.result().edit_text = MagicMock()
        view.update("updated")
        args, kwargs = view.raw_object.result().edit_text.call_args
        self.assertEqual(args[0], "updated\n\U000e0020 ")

    def test_delete(self):
        view = TelegramTextView(self.session.view_container, "test")
        view.draw()
        view.raw_object.result().delete = MagicMock()

        temp = view.raw_object
        view.remove()
        temp.result().delete.assert_called_with()
