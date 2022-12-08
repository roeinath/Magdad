from typing import Optional
import vobject

from bot_framework.Telegram.View.telegram_view_container import TelegramViewContainer
from bot_framework.View.contact_view import ContactView


class TelegramContactView(ContactView):

    def __init__(self, view_container: TelegramViewContainer, name: str="", phone: str="", email: str = None):
        super().__init__(view_container, name, phone, email)

        self.view_container = view_container

    def draw(self):
        super().draw()

        # Get the chat id of the session (which is unique for a user)
        chat_id = self.get_session().user.telegram_id
        # Send the message using the raw_bot reference to the chat id from the session.
        vcard = self._get_vcard()
        self.raw_object = self.view_container.ui.raw_bot.send_contact(
            self.get_session(), chat_id, first_name=self.name, phone_number=self.phone, vcard=vcard
        )

    def update(self, name: str = "", phone: str = "", email: str = None):
        super().update(name, phone)
        raise NotImplementedError()

    def remove_raw(self):
        if self.raw_object.result() is not None:
            self.raw_object.result().delete()

    def _get_vcard(self) -> Optional[str]:
        if self.email is None:
            return None

        j = vobject.vCard()
        j.add('fn').value = self.name
        j.add('email').value = self.email
        o = j.add('tel')
        o.type_param = "cell"
        o.value = self.phone

        return j.serialize()
