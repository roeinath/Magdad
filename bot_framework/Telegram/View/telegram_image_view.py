from bot_framework.Telegram.View.telegram_view_container import TelegramViewContainer
from bot_framework.View.image_view import ImageView


class TelegramImageView(ImageView):
    def __init__(self, view_container: TelegramViewContainer, text: str="", img_src: str=""):
        super().__init__(view_container, text, img_src)

        self.view_container = view_container

    def draw(self):
        super().draw()

        # Get the chat id of the session (which is unique for a user)
        chat_id = self.get_session().user.telegram_id

        # Send the message using the raw_bot reference to the chat id from the session.
        try:
            img = open(self.img_src, 'rb')
        except FileNotFoundError:
            img = []

        self.raw_object = self.view_container.ui.raw_bot.send_photo(self.get_session(), chat_id, caption=self.text, photo=img)

    def update(self, new_text: str, new_img_src: str):
        super().update(new_text, new_img_src)

        self.raw_object.result().edit_caption(caption=new_text)

    def remove_raw(self):
        if self.raw_object.result() is not None:
            self.raw_object.result().delete()
