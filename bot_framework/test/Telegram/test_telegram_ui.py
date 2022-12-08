import unittest
from unittest.mock import MagicMock

from bot_framework.session import Session
from bot_framework.Telegram.telegram_ui import TelegramUI
from bot_framework.Telegram.View.telegram_text_view import TelegramTextView
from bot_framework.test.mock_container import MockContainer
from bot_framework.test.test_bot_user import TestBotUser
from bot_framework.ui.ui import UI


class TestTelegramUI(unittest.TestCase):

    @staticmethod
    def add_handler_mock(handler):
        handler.callback(None, None)

    @classmethod
    def setUpClass(cls) -> None:
        bot = MockContainer()
        bot.send_photo = MagicMock()
        bot.send_message = MagicMock()
        bot.send_contact = MagicMock()

        dispatcher = MockContainer()
        cls.handlers = []
        dispatcher.add_handler = lambda h: cls.handlers.append(h)

        cls.ui = TelegramUI(bot, dispatcher, TestBotUser, True)

        u = MockContainer()
        u.telegram_id = "test_id"
        u.id = "test_id_r"

        cls.user = u
        cls.session = cls.ui.create_session("Testing", u)

    def test_get_photo(self):
        func = self.handlers[0]

        function_called = MagicMock()
        self.ui.get_photo(self.session, function_called)

        update = MockContainer()
        update.effective_user = self.session.user
        update.message = MockContainer()
        update.message.photo = [MockContainer()]

        real_photo = MockContainer
        update.message.photo[0].get_file = lambda: real_photo

        func(update, None)
        function_called.assert_called_with(self.session, real_photo)

    def test_get_text(self):
        func = self.handlers[1]

        function_called = MagicMock()
        self.ui.get_text(self.session, function_called)

        update = MockContainer()
        update.effective_user = self.user
        update.message = MockContainer()
        update.message.text = "hi"

        func(update, None)
        function_called.assert_called_with(self.session, update.message.text)

    def test_get_document(self):
        func = self.handlers[2]

        function_called = MagicMock()
        self.ui.get_document(self.session, function_called)

        update = MockContainer()
        update.effective_user = self.session.user
        update.message = MockContainer()
        update.message.document = MockContainer()

        real_file = MockContainer
        update.message.document.get_file = lambda: real_file

        func(update, None)
        function_called.assert_called_with(self.session, real_file)

    def test_clear(self):
        text = self.ui.create_text_view(self.session, "test")
        text.draw()

        text.remove = MagicMock()

        self.ui.clear(self.session)

        text.remove.assert_called_with()

    def test_create_text_view(self):
        text = self.ui.create_text_view(self.session, "test")
        self.assertEqual(text.text, "test")
        self.assertEqual(text.view_container, self.session.view_container)

    def test_create_button_group_view(self):
        buttons = [self.ui.create_button_view("b1", lambda s: None), self.ui.create_button_view("b2", lambda s: None)],

        group = self.ui.create_button_group_view(self.session, "test", buttons)
        self.assertEqual(group.text, "test")
        self.assertEqual(group.buttons, buttons)


    def test_create_button_matrix_view(self):
        buttons = [
            [self.ui.create_button_view("b1", lambda s: None), self.ui.create_button_view("b2", lambda s: None)],
            [self.ui.create_button_view("b3", lambda s: None)]
        ]
        matrix = self.ui.create_button_matrix_view(self.session, "test", buttons)
        self.assertEqual(matrix.text, "test")
        self.assertEqual(matrix.buttons, buttons)

    def test_create_image_view(self):
        photo = self.ui.create_image_view(self.session, "test", "test.png")
        self.assertEqual(photo.view_container, self.session.view_container)
        self.assertEqual(photo.text, "test")

    def test_create_contact_view(self):
        contact = self.ui.create_contact_view(self.session, "Testing McTest", "1234567890", "test@test.test")
        self.assertEqual(contact.name, "Testing McTest")
        self.assertEqual(contact.phone, "1234567890")
        self.assertEqual(contact.email, "test@test.test")

    def test_create_location_view(self):
        location = self.ui.create_location_view(self.session, "test_location", 100, 200)
        self.assertEqual(location.text, "test_location")
        self.assertEqual(location.latitude, 100)
        self.assertEqual(location.longitude, 200)

    def test_create_text_list_view(self):
        ls = ["t1", "t2","t3","t4","t5","t6","t7","t8","t9","t10","t11","t12","t13", "t14","t15","t16","t17","t18","t19","t20","t21","t22","t23","t24","t25", ]
        lss = self.ui.create_text_list_view(self.session, "test_title", ls)

        if len(ls) > UI.MAX_LIST_LEN:
            ls = ls[:UI.MAX_LIST_LEN]
            ls.append(f'מציג רק ' + f'{UI.MAX_LIST_LEN}' + ' ראשונים')
        text = f"*test_title*" + "\n▪ " + "\n▪ ".join(ls)

        self.assertEqual(lss.text, text)

    def test_summarize_and_close(self):
        original_view = self.ui.create_text_view(self.session, "hi")
        original_view.draw()
        original_view.remove = MagicMock()

        view = TelegramTextView(self.session.view_container, "closed")
        view.draw = MagicMock()


        self.ui.summarize_and_close(self.session, [view])
        original_view.remove.assert_called()
        self.assertFalse(self.session.active)
        self.assertNotIn(self.session, Session.sessions[self.user.id])
        view.draw.assert_called()




