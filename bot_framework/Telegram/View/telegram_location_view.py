from bot_framework.Telegram.View.telegram_view_container import TelegramViewContainer
from bot_framework.View.location_view import LocationView


class TelegramLocationView(LocationView):

    def __init__(self, view_container: TelegramViewContainer, text: str='', latitude: float=0, longitude: float=0):
        super().__init__(view_container, text, latitude, longitude)

        self.view_container: TelegramViewContainer = view_container

    def draw(self):
        super().draw()

        # Get the chat id of the session (which is unique for a user)
        chat_id = self.get_session().user.telegram_id

        # Send the message using the raw_bot reference to the chat id from the session.
        self.raw_object = self.view_container.ui.raw_bot.send_location(
            self.get_session(), chat_id, caption=self.text,
            latitude=self.latitude, longitude=self.longitude
        )

    def update(self, new_text: str):
        super().update(new_text)

        self.raw_object.result().edit_caption(caption=new_text)
        # view.raw_object.result().edit_media(open(new_img_src, 'rb'))

    def remove_raw(self):
        if self.raw_object.result() is not None:
            self.raw_object.result().delete()
