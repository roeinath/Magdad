from typing import Callable, Dict, Type
from abc import *

from datetime import date, datetime

from telegram import File

from bot_framework.Activity.FormActivity.form_activity import FormActivity
from bot_framework.Activity.closest_name_activity import ClosestNameActivity
from bot_framework.Activity.strings_choose_activity import StringsChooseActivity
from bot_framework.Activity.names_choose_activity import NamesChooseActivity
from bot_framework.View.button_group_view import ButtonGroupView
from bot_framework.View.button_matrix_view import ButtonMatrixView
from bot_framework.View.contact_view import ContactView
from bot_framework.Activity.date_choose_activity import DateChooseView
from bot_framework.View.dice_view import DiceView
from bot_framework.View.image_view import ImageView
from bot_framework.View.location_view import LocationView
from bot_framework.View.text_view import TextView
from bot_framework.Activity.time_choose_activity import TimeChooseView
from bot_framework.View.view_container import ViewContainer
from bot_framework.session import Session
from bot_framework.ui.button import Button
from bot_framework.bot_user import BotUser


class UI(ABC):
    MAX_LIST_LEN = 15

    # Initialize the ui
    def __init__(self):
        """
        Initialize the UI of the bot (called once, when the bot is created. Handles all users and sessions).
        """
        # Save reference to the raw bot (for sending messages).
        super().__init__()
        # Next free button id. Every button has a unique ID that will be sent to the server
        # when it is clicked.
        self.next_id = '0'
        # A list of all buttons sent.
        self.buttons = {}
        # Stacks of get_text methods for each user. The newest text receiver is the current one that will be called
        # when the user sends a message. Each user has a stack.
        self.user_stacks = {}
        self.user_photo_stacks = {}
        self.user_document_stacks = {}

    def create_session(self, feature_name: str, user: BotUser) -> Session:
        """
        Creates and returns a new session for the given
        feature_name and User
        :param feature_name: The feature name for the Session
        :param user: The user for the Session
        :return: Created session object
        """
        return Session(feature_name, user, self)

    # @abstractmethod
    # def create_popup_session(self, feature_name: str, user: BotUser, callback) -> None:
    #     """
    #     Creates and returns a new session for the given
    #     feature_name and User
    #     :param feature_name: The feature name for the Session
    #     :param user: The user for the Session
    #     :param callback: callback function to call after getting permission to create the session
    #     :return: Created session object
    #     """
    #     pass

    def get_photo(self, session: Session, func_to_call: Callable[[Session, File], None]) -> None:
        """
        Create a new photo listener. func_to_call will be called when the user sends a photo.
        :param session: the session that the user to receive text from will be extracted from
        :param func_to_call: the function to call and pass the received photo to.
        """

        if not isinstance(func_to_call, Callable):
            raise Exception("func_to_call must be callable in get_text")

        # Get the user to listen to from the session object
        user = session.user
        # Create a listener stack if one doesn't exist yet
        if user not in self.user_photo_stacks:
            self.user_photo_stacks[user] = []
        # Add the func_to_call to the stack
        self.user_photo_stacks[user].insert(0, (func_to_call, session))

        # Create a new text listener. func_to_call will be called when the user writes text.

    # Create a new text listener. func_to_call will be called when the user writes text.

    def get_document(self, session: Session, func_to_call: Callable[[Session, File], None]) -> None:
        """
        Create a new document listener. func_to_call will be called when the user sends a document.
        :param session: the session that the user to receive document from will be extracted from
        :param func_to_call: the function to call and pass the received document to.
        """

        if not isinstance(func_to_call, Callable):
            raise Exception("func_to_call must be callable in get_text")

        # Get the user to listen to from the session object
        user = session.user
        # Create a listener stack if one doesn't exist yet
        if user not in self.user_document_stacks:
            self.user_document_stacks[user] = []
        # Add the func_to_call to the stack
        self.user_document_stacks[user].insert(0, (func_to_call, session))

    def get_text(self, session: Session, func_to_call: Callable[[Session, str], None]) -> None:
        """
        Create a new text listener. func_to_call will be called when the user writes text.
        :param session: the session that the user to receive text from will be extracted from
        :param func_to_call: the function to call and pass the received text to.
        """

        if not isinstance(func_to_call, Callable):
            raise Exception("func_to_call must be callable in get_text")

        # Get the user to listen to from the session object
        user = session.user
        # Create a listener stack if one doesn't exist yet
        if user not in self.user_stacks:
            self.user_stacks[user] = []
        # Add the func_to_call to the stack
        self.user_stacks[user].insert(0, (func_to_call, session))

    def clear(self, session: Session) -> None:
        """
        Clear all the views in this session (delete every text message and button.
        :param session: the session to clear views from.
        """

        session.view_container.remove()

    @abstractmethod
    def create_text_view(self, session: Session, text: str,
                         view_container: ViewContainer = None) -> TextView:
        """
        Create a text view object for sending on this ui
        :param session: the session to send on top of
        :param text: the text to send
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return: the view object created
        """
        pass

    @abstractmethod
    def create_button_group_view(self, session: Session, title: str, buttons: [Button],
                                 view_container: ViewContainer = None) -> ButtonGroupView:
        """
        Create a button group view object for sending on this ui
        :param session: the session to send on top of
        :param title: the text to send
        :param buttons: the buttons to send
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return: the view object created
        """
        pass

    @abstractmethod
    def create_button_matrix_view(self, session: Session, title: str,
                                  buttons: [Button],
                                  view_container: ViewContainer = None) -> ButtonMatrixView:
        """
        Create a button matrix view object for sending on this ui
        :param session: the session to send on top of
        :param title: the text to send
        :param buttons: the buttons to send
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return: the view object created
        """
        pass

    @abstractmethod
    def create_contact_view(self, session: Session, name: str, phone: str, email: str = None,
                            view_container: ViewContainer = None) -> ContactView:
        """
        Create a contact view object for sending on this ui
        :param session: the session to send on top of
        :param name: the text to send
        :param phone: the phone number to send
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return: the view object created
        """
        pass

    @abstractmethod
    def create_image_view(self, session: Session, title: str, img_src: str,
                          view_container: ViewContainer = None) -> ImageView:
        """
        Create an image view object for sending on this ui
        :param session: the session to send on top of
        :param title: the text to send
        :param img_src: the source of the image to send
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return: the view object created
        """
        pass

    @abstractmethod
    def create_location_view(self, session: Session, text: str, latitude: float, longitude: float,
                             view_container: ViewContainer = None) -> LocationView:
        """
        Create an location view object for sending on this ui
        :param session: the session to send on top of
        :param text: The text to send
        :param latitude: Latitude of location
        :param longitude: Longitude of location
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return:
        """
        pass

    @abstractmethod
    def create_dice_view(self, session, view_container: ViewContainer = None) -> DiceView:
        pass

    def create_text_list_view(self, session: Session, title: str, list_items: [str],
                              view_container: ViewContainer = None) -> TextView:
        if len(list_items) > UI.MAX_LIST_LEN:
            list_items = list_items[:UI.MAX_LIST_LEN]
            list_items.append(f'מציג רק ' + f'{UI.MAX_LIST_LEN}' + ' ראשונים')
        text = f"*{title}*" + "\n▪ " + "\n▪ ".join(list_items)

        return self.create_text_view(session, text)

    # noinspection PyMethodMayBeStatic
    def create_button_view(self, title: str, callback: Callable[[Session], None]) -> Button:
        """
        Creates a button with a specific title and callback.
        :param title:
        :param callback:
        :return:
        """
        return Button(title, callback)

    def create_date_choose_view(self, session: Session,
                                choose_callback: Callable[[DateChooseView, Session, date], None],
                                chosen_date: date = None,
                                view_container: ViewContainer = None, title: str = "בחר תאריך") -> DateChooseView:
        view_container = view_container if view_container is not None else session.view_container

        return DateChooseView(view_container, choose_callback, chosen_date, title=title)

    def create_time_choose_view(self, session: Session,
                                choose_callback: Callable[[TimeChooseView, Session, datetime], None],
                                chosen_time: datetime = None,
                                view_container: ViewContainer = None):
        view_container = view_container if view_container is not None else session.view_container

        return TimeChooseView(view_container, choose_callback, chosen_time)

    def create_closest_name_view(self, session: Session, data: Dict[str, object], key: str, count: int,
                                 choose_callback: Callable[[Session, object], None],
                                 try_again: Callable[[Session], None],
                                 view_container: ViewContainer = None):
        view_container = view_container if view_container is not None else session.view_container

        return ClosestNameActivity(view_container, data, key, count, choose_callback, try_again)

    def create_names_choose_view(self, session: Session, submit_callback: Callable[[Session, list], None],
                                 from_names: [str] = None, max_buttons: int = 6,
                                 view_container: ViewContainer = None):
        view_container = view_container if view_container is not None else session.view_container

        from_names = from_names if from_names is not None else []
        return NamesChooseActivity(view_container, submit_callback, from_names=from_names, max_buttons=max_buttons)

    def create_form_view(self, session: Session, form_object, name: str, callback: Callable,
                                 view_container: ViewContainer = None):

        view_container = view_container if view_container is not None else session.view_container
        return FormActivity(view_container, form_object, name, callback)

    def clear_feature_sessions_user(self, feature_name: str, user: BotUser):
        """
        Clears all session with the given feature_name for the
        given user.
        :param feature_name: The feature name to search for
        :param user: The user to search for
        :return:
        """

        if user.id not in Session.sessions:
            return

        for (session_id, session) in Session.sessions[user.id].items():
            if session.feature_name == feature_name:
                self.clear(session)

    def summarize_and_close(self, session: Session, views=None):
        """
        Summerize a session, clear it, and delete it.
        :param session: session to clear
        :param views: the views to send as a summary
        :param prompt_menu: true if a menu prompt should be sent in addition to the summary
        """
        if views is None:
            views = []
        if session is None:
            return

        try:
            self.clear(session)
        except Exception as e:
            print("Session clear threw an exception: ", e)
            print("The exception was ignored and the session not cleared, to avoid crashing the bot.")
            return
        session.active = False

        try:
            Session.delete_session(session)
        except Exception as e:
            print("Session deletion threw an exception: ", e)
            print("The exception was ignored and the session not deleted, to avoid crashing the bot.")

        # Check for references to session outside of this call.
        """debug_ = gc.get_referrers(session)
        if len(debug_ > 1):
            print("Session should be deleted but still has references.")
            print("To stop this message, remove the debugging code from TelegramUI.summarize_and_close")
            print(debug_)"""

        if views is not None:
            for view in views:
                try:
                    view.draw()
                except Exception as e:
                    import traceback
                    print("ERROR - couldn't draw the summary of a session.")
                    print("This error was ignored and the view was not drawn, to avoid crashing the bot")
