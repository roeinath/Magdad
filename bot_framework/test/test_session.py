import unittest
from unittest.mock import MagicMock

from bot_framework.session import Session
from bot_framework.Telegram.telegram_ui import TelegramUI
from bot_framework.TestKit import TestKitUI
from bot_framework.View.view_container import ViewContainer
from bot_framework.bot_user import BotUser
from bot_framework.test.test_bot_user import TestBotUser


class TestSession(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_ui = TestKitUI()
        cls.session = Session("testing", TestBotUser("123", "456"), cls.test_ui)

    def test_add_button(self):
        prev_id = self.session.next_id
        func = MagicMock()
        got_id = self.session.add_button(func)
        self.assertEqual(self.session.next_id, str(int(prev_id) + 1))

        self.session.buttons[got_id](None)
        func.assert_called()
        self.assertEqual(self.session.buttons[got_id], func)

    def test_generate_id(self):
        id1 = Session.generate_id()
        id2 = Session.generate_id()
        self.assertNotEqual(id1, id2)

    def test_create_session(self):
        session = self.session
        self.assertEqual(session.user, self.session.user)
        self.assertEqual(session.feature_name, "testing")
        self.assertIsInstance(session.data, dict)
        self.assertIsInstance(session.view_container, ViewContainer)
        self.assertIsInstance(session.buttons, dict)
        self.assertEqual(session.next_id, "1")
        self.assertEqual(session.active, True)

        # Test that register works
        self.assertIn(session.user.id, Session.sessions)
        self.assertIn(session.id, Session.sessions[session.user.id])
        self.assertEqual(Session.sessions[session.user.id][session.id], session)

    def test_delete_session(self):
        session = Session("testing", self.session.user, TestSession.test_ui)
        Session.register_session(session)
        Session.delete_session(session)
        self.assertEqual(len(session.buttons), 0)
        self.assertNotIn(session, Session.sessions[session.user.id])

    def test_get_random_id_token(self):
        id1 = Session.gen_random_id_token()
        id2 = Session.gen_random_id_token()
        self.assertNotEqual(id1, id2)


