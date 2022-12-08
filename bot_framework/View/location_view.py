from __future__ import annotations
from bot_framework.View.view import View
from bot_framework.View.view_container import ViewContainer


class LocationView(View):
    def __init__(self, view_container: ViewContainer, text: str='', latitude: float=0, longitude: float=0):
        super().__init__(view_container)
        self.latitude = latitude
        self.longitude = longitude
        self.text = text

    def update(self, text):
        super().update()

        if text == self.text:
            raise Exception("Cant update a view with the same details.")

        self.text = text

    def remove_raw(self):
        pass

    def __eq__(self, other: LocationView):
        """Overrides the default implementation"""
        if isinstance(other, LocationView):
            return self.text == other.text and\
                   self.latitude == other.latitude and\
                   self.longitude == other.longitude

        return False
