from __future__ import annotations
import typing

from bot_framework.View.view_container import ViewContainer

if typing.TYPE_CHECKING:
    from bot_framework.session import Session
    from bot_framework.Telegram.telegram_ui import TelegramUI


class TelegramViewContainer(ViewContainer):
    def __init__(self, session: Session, ui: TelegramUI):
        super().__init__(session, ui)

        self.ui = ui
