from bot_framework.View.button_group_view import ButtonGroupView
from bot_framework.View.button_matrix_view import ButtonMatrixView
from bot_framework.View.contact_view import ContactView
from bot_framework.View.dice_view import DiceView
from bot_framework.View.image_view import ImageView
from bot_framework.View.location_view import LocationView
from bot_framework.View.text_view import TextView
from bot_framework.View.view_container import ViewContainer
from bot_framework.session import Session
from bot_framework.ui.ui import UI


class TestKitUI(UI):
    def put_text(self, text: str):
        pass

    def create_text_view(self, session: Session, text: str, view_container: ViewContainer = None) -> TextView:
        """
        Create a text view object for sending on this ui
        :param session: the session to send on top of
        :param text: the text to send
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return: the view object created
        """

        return TextView(view_container, text)

    def create_button_group_view(self, session: Session, title: str, buttons, view_container: ViewContainer = None) -> ButtonGroupView:
        """
        Create a button group view object for sending on this ui
        :param session: the session to send on top of
        :param title: the text to send
        :param buttons: the buttons to send
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return: the view object created
        """
        view_container = view_container if view_container is not None else session.view_container

        return ButtonGroupView(view_container, title, buttons)

    def create_button_matrix_view(self, session: Session, title: str, buttons, view_container: ViewContainer = None) -> ButtonMatrixView:
        """
        Create a button matrix view object for sending on this ui
        :param session: the session to send on top of
        :param title: the text to send
        :param buttons: the buttons to send
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return: the view object created
        """
        view_container = view_container if view_container is not None else session.view_container

        return ButtonMatrixView(view_container, title, buttons)

    def create_contact_view(self, session: Session, name: str, phone: str, email: str = None, view_container: ViewContainer = None) -> ContactView:
        """
        Create a contact view object for sending on this ui
        :param session: the session to send on top of
        :param name: the text to send
        :param phone: the phone number to send
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return: the view object created
        """
        view_container = view_container if view_container is not None else session.view_container

        return ContactView(view_container, name, phone, email)

    def create_image_view(self, session: Session, title: str, img_src: str, view_container: ViewContainer = None) -> ImageView:
        """
        Create an image view object for sending on this ui
        :param session: the session to send on top of
        :param title: the text to send
        :param img_src: the source of the image to send
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return: the view object created
        """
        view_container = view_container if view_container is not None else session.view_container

        return ImageView(view_container, title, img_src)

    def create_location_view(self, session: Session, text: str, latitude: float,
                             longitude: float, view_container: ViewContainer = None) -> LocationView:
        """
        Create an location view object for sending on this ui
        :param session: the session to send on top of
        :param title: the text to send
        :param img_src: the source of the image to send
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return: the view object created
        """
        view_container = view_container if view_container is not None else session.view_container

        return LocationView(view_container, text=text, longitude=longitude, latitude=latitude)

    def create_dice_view(self, session, view_container: ViewContainer = None) -> DiceView:
        """
        Creates a random dice view
        :param self:
        :param session:
        :param view_container:
        :return:
        """
        view_container = view_container if view_container is not None else session.view_container

        return DiceView(view_container)
