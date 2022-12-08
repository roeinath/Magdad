import unittest

from APIs.TalpiotSystem import Vault, TalpiotSettings
from APIs.TalpiotSystem import UserPassCredentials
from APIs.TalpiotAPIs import User


class TestVault(unittest.TestCase):

    def test_get_vault(self):
        v = Vault.get_vault(True)
        self.assertIsInstance(v, Vault)

        self.assertEqual(v, Vault.get_vault())

        self.assertEqual(len(v.tokens), 2)
        self.assertEqual(len(v.user_pass), 2)

    def test_get_token(self):
        v = Vault.get_vault(True)
        self.assertEqual(v.get_token("BOT_TOKEN"), 9999)
        self.assertEqual(v.get_token("TEST_TOKEN"), 1234)

    def test_get_user_pass(self):
        v = Vault.get_vault(True)

        creds = v.get_user_pass("DB_ACCESS")
        self.assertIsInstance(creds, UserPassCredentials)
        self.assertEqual(creds.user, "bot_readonly_user")
        self.assertEqual(creds.password, "P+8+h0tR4CPE9da3q4W7eg==")

        creds = v.get_user_pass("GDRIVE")
        self.assertIsInstance(creds, UserPassCredentials)
        self.assertEqual(creds.user, "test@test.test")
        self.assertEqual(creds.password, 1234)

    def test_db(self):
        v = Vault.get_vault(True)

        if not TalpiotSettings.isset():
            TalpiotSettings()

        v.connect_to_db()
        self.assertGreater(len(User.objects), 0)

