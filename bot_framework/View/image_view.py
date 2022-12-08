from __future__ import annotations
from bot_framework.View.view import View
from bot_framework.View.view_container import ViewContainer


class ImageView(View):

    def __init__(self, view_container: ViewContainer, text: str="", img_src: str=""):
        super().__init__(view_container)
        self.text = text
        self.img_src = img_src

    def update(self, new_text: str, new_img_src: str):
        super().update()

        if new_text == self.text and self.img_src == new_img_src:
            raise Exception("Cant update a view with the same details.")

        self.text = new_text
        self.img_src = new_img_src

    def remove_raw(self):
        pass

    def __eq__(self, other: ImageView):
        """Overrides the default implementation"""
        if isinstance(other, ImageView):
            return self.text == other.text and\
                   self.img_src == other.img_src

        return False
