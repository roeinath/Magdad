from APIs.ExternalAPIs.Mail.system_mail_client import MailClient
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.User.who_is import get_user_by_secret_code


class SecretCodeManager:
    # 12 alphanumeric chars
    CODE_REGEX = r"^[a-zA-Z0-9]{25}$"

    def __init__(self):
        pass

    @staticmethod
    def get_token_regex():
        return

    @staticmethod
    def get_user_by_secret_code(secret_code):
        return get_user_by_secret_code(secret_code)

    @staticmethod
    def generate_code():
        import rstr
        return rstr.xeger(SecretCodeManager.CODE_REGEX)

    @staticmethod
    def generate_codes():
        # connect_db_readonly_access()
        users_without_code = User.objects.filter(secret_code=None)
        for user in users_without_code:
            user.secret_code = SecretCodeManager.generate_code()
            user.save()

    @staticmethod
    def send_code_to_users(users: [User]):
        client = MailClient()
        client.connect()
        for user in users:
            SecretCodeManager.send_code_to_user(client, user)
        client.close()

    @staticmethod
    def send_code_to_user(mail_client, user):
        msg = f"Hi {user.name}!\n\n"
        msg += f"This is your secret code: {user.secret_code}\n"
        msg += f"Use it to log in to the system.\n\n"
        msg += f"Thank you, the TalpiX team."
        print(msg)
        mail_client.send_mail(user.email, "TalpiBot Secret Code", msg)

    @staticmethod
    def genereate_secret_url(bot_user_name, code):
        return f"telegram.me/{bot_user_name}?start={code}"

    @staticmethod
    def send_url_to_users(users: [User], bot_user_name):
        client = MailClient()
        client.connect()
        for user in users:
            SecretCodeManager.send_url_to_user(client, user, bot_user_name)
        client.close()

    @staticmethod
    def send_url_to_user(mail_client, user, bot_user_name):
        msg = f"Hi {user.name}!\n\n"
        msg += f"This is your secret link:\n {SecretCodeManager.genereate_secret_url(bot_user_name, user.secret_code)}\n"
        msg += f"Use it to log in to the system.\n\n"
        msg += f"Thank you, the TalpiX team."
        print(msg)
        mail_client.send_mail(user.email, "TalpiBot Secret Code", msg)


def test_class():

    non_codes = User.objects.filter(name="שירי מזרחי")
    SecretCodeManager.generate_codes()
    shiri = non_codes[0]
    print(shiri.name)
    print(SecretCodeManager.genereate_secret_url("TalpiBot", shiri.secret_code))

    # connect_db_readonly_access()
    # users = User.objects.filter(name='דוד אורן')
    # print(SecretCodeManager.genereate_secret_url("TalpiBot", users[0].secret_code))
    # print(SecretCodeManager.genereate_secret_url("TalpiBot", users[0].secret_code))
    # SecretCodeManager.send_url_to_users(users, "TalpiBot")


if __name__ == '__main__':
    from settings import load_settings
    from APIs.TalpiotSystem import Vault

    load_settings()
    # Vault.get_vault().connect_to_db()
    test_class()
