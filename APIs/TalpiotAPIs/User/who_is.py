from typing import Callable, Any, Optional
import APIs.TalpiotAPIs.User.user as user
from APIs.TalpiotAPIs.User.user import User


def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
    """
    Returns a user from an TelegramId, that is recieved
    from the telegram bot library, on request.

    :param telegram_id: the telegramId of the user
    :return: User object or None if not found.
    """

    try:
        return User.objects.get(telegram_id=telegram_id)
    except user.DoesNotExist:
        return None



def get_user_by_name(user_name: int) -> Optional[User]:
    """
    Returns a user from an Name, that is recieved
    from the telegram bot library, on request.

    :param user_name: the name of the user
    :return: User object or None if not found.
    """

    try:
        return User.objects.get(name=user_name)
    except user.DoesNotExist:
        return None


def get_user_by_secret_code(secret_code: str) -> Optional[User]:
    """
    Returns a user from a secret code, that is recieved
    from the telegram bot library, on request.

    :param secret code: the secret code of the user
    :return: User object or None if not found.
    """

    try:
        return User.objects.get(secret_code=secret_code)
    except user.DoesNotExist:
        return None
