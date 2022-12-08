import unittest
from unittest.mock import MagicMock

from bot_framework.session import Session
from bot_framework.Telegram.telegram_ui import TelegramUI
from bot_framework.Telegram.View.telegram_contact_view import TelegramContactView
from bot_framework.test.mock_container import MockContainer
from bot_framework.test.test_bot_user import TestBotUser



class TestTelegramContactView(unittest.TestCase):

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
        view = TelegramContactView(self.session.view_container, "test_contact", "1234567890", "test@test.test")
        view.draw()

        args, kwargs = self.ui.raw_bot.send_contact.call_args
        self.assertEqual(args[0], self.session)
        self.assertEqual(args[1], self.user.telegram_id)
        self.assertEqual(kwargs["first_name"], "test_contact")
        self.assertEqual(kwargs["phone_number"], "1234567890")

    def test_update(self):
        # ContactView.update is not implemented, contact messages can't be edited?
        pass

    def test_delete(self):
        view = TelegramContactView(self.session.view_container, "test_contact", "1234567890", "test@test.test")
        view.draw()

        view.raw_object.result().delete = MagicMock()

        temp = view.raw_object
        view.remove()
        temp.result().delete.assert_called_with()
