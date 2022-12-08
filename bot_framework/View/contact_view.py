from __future__ import annotations
from bot_framework.View.view import View
from bot_framework.View.view_container import ViewContainer


class ContactView(View):

    def __init__(self, view_container: ViewContainer, name: str="", phone: str="", email: str = None):
        super().__init__(view_container)
        self.name = name
        self.phone = phone
        self.email = email

    def update(self, name: str = "", phone: str = "", email: str = None):
        super().update()

        if name == self.name and self.phone == phone and self.email == email:
            raise Exception("Cant update a view with the same details.")

        self.name = name
        self.phone = phone
        self.email = email

    def remove_raw(self):
        pass

    def __eq__(self, other: ContactView):
        """Overrides the default implementation"""
        if isinstance(other, ContactView):
            return self.name == other.name and\
                   self.phone == other.phone and\
                   self.email == other.email

        return False
