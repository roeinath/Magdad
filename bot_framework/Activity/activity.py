from abc import abstractmethod
from bot_framework.View.drawable import Drawable
from bot_framework.View.view_container import ViewContainer


class Activity(Drawable):

    def __init__(self, view_container: ViewContainer):
        """
        Create a view that will be drawn using the given UI and belong to the given session
        :param ui: ui to draw the view on when draw() is called
        :param session: session this view belongs to
        """
        self.view_container = view_container
        self.drawn = False

    def draw(self):
        """
        Draw this view on the ui
        """
        if self.view_container is not None:
            self.view_container.views.append(self)

        self.drawn = True

    def update(self, *params):
        """
        update the view with new parameters
        :param params: new parameters (i.e new text for text_view).
        """
        if not self.drawn:
            raise Exception("View updated before drawn. Use view.draw() first.")

    def is_sent(self):
        """
        Check if this view was drawn already
        :return: True if this view was drawn, False otherwise.
        """
        return self.drawn

    def remove(self) -> bool:
        """
        Remove this view from the session and from the ui
        :return: True if the removal succeeded and False otherwise.
        """
        if not self.drawn:
            return False

        self.remove_raw()
        self.view_container.views.remove(self)

        return True

    @abstractmethod
    def remove_raw(self):
        """
        Remove the actual message from the ui. subclass responsibility.
        """
        pass
