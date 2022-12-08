from typing import Callable, Type
import telegram
from telegram import File

from bot_framework.Telegram.View.telegram_view_container import TelegramViewContainer
from bot_framework.Telegram.telegram_queued_bot import TelegramQueuedBot

from bot_framework.Telegram.View.telegram_button_group_view import TelegramButtonGroupView
from bot_framework.Telegram.View.telegram_button_matrix_view import TelegramButtonMatrixView
from bot_framework.Telegram.View.telegram_contact_view import TelegramContactView
from bot_framework.Telegram.View.telegram_dice_view import TelegramDiceView
from bot_framework.Telegram.View.telegram_image_view import TelegramImageView
from bot_framework.Telegram.View.telegram_location_view import TelegramLocationView
from bot_framework.Telegram.View.telegram_text_view import TelegramTextView
from bot_framework.Telegram.telegram_session import TelegramSession
from bot_framework.crash_logger import log_all_exceptions
from bot_framework.session import Session
from bot_framework.bot_logger import BotLogger
from bot_framework.bot_user import BotUser
from telegram.ext import CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext.dispatcher import run_async, Dispatcher
from bot_framework.ui.ui import UI


# UI Methods for interfacing with the telegram API. Inherits everything from the base UI class.
class TelegramUI(UI):

    # Initialize the ui
    def __init__(self, raw_bot: TelegramQueuedBot, dispatcher: Dispatcher, user_type: Type[BotUser], test=False):
        """
        Initialize the UI of the bot (called once, when the bot is created. Handles all users and sessions).
        :param raw_bot: the bot object given by the telegram  API
        :param dispatcher: the dispacher object given by the telgram API (used for adding button press events).
        """
        # Save reference to the raw bot (for sending messages).
        super().__init__()
        self.raw_bot: TelegramQueuedBot = raw_bot
        # Save reference to the dispatcher (for adding button events).
        self.dispatcher = dispatcher

        self.user_type = user_type

        self.test = test
        # create handlers for both text and buttons
        self.create_handlers()

    def create_session(self, feature_name: str, user: BotUser) -> TelegramSession:
        """
        Creates and returns a new session for the given
        feature_name and User
        :param feature_name: The feature name for the Session
        :param user: The user for the Session
        :return: Created session object
        """
        return TelegramSession(feature_name, user, self)

    def create_popup_session(self, feature_name: str, user: BotUser, callback) -> None:
        """
        Creates and returns a new session for the given
        feature_name and User
        :param feature_name: The feature name for the Session
        :param user: The user for the Session
        :param callback: callback function to call after getting permission to create the session
        :return: Created session object
        """
        session = TelegramSession(feature_name, user, self)
        index = Session.sessions[user.id]
        if len(index) == 1:
            callback(session)
        else:
            buttons = [self.create_button_view("אישור", lambda s: callback(session))]
            self.create_button_group_view(buttons=buttons, session=session,
                                          title="פיצ'ר {0} רוצה לשלוח לך הודעה".format(feature_name)).draw()

    def create_text_view(self, session: Session, text: str,
                         view_container: TelegramViewContainer = None) -> TelegramTextView:
        """
        Create a text view object for sending on this ui
        :param session: the session to send on top of
        :param text: the text to send
        :param view_container: (Not required) the view container to draw the view in. If None, uses
        the session default view_container. Will be used mostly for Activities
        :return: the view object created
        """
        view_container = view_container if view_container is not None else session.view_container

        return TelegramTextView(view_container, text)

    def create_button_group_view(self, session: Session, title: str, buttons,
                                 view_container: TelegramViewContainer = None) -> TelegramButtonGroupView:
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

        return TelegramButtonGroupView(view_container, title, buttons)

    def create_button_matrix_view(self, session: Session, title: str, buttons,
                                  view_container: TelegramViewContainer = None) -> TelegramButtonMatrixView:
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

        return TelegramButtonMatrixView(view_container, title, buttons)

    def create_contact_view(self, session: Session, name: str, phone: str, email: str = None,
                            view_container: TelegramViewContainer = None) -> TelegramContactView:
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

        return TelegramContactView(view_container, name, phone, email)

    def create_image_view(self, session: Session, title: str, img_src: str,
                          view_container: TelegramViewContainer = None) -> TelegramImageView:
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

        return TelegramImageView(view_container, title, img_src)

    def create_location_view(self, session: Session, text: str, latitude: float,
                             longitude: float, view_container: TelegramViewContainer = None) -> TelegramLocationView:
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

        return TelegramLocationView(view_container, text=text, longitude=longitude, latitude=latitude)

    def create_dice_view(self, session, view_container: TelegramViewContainer = None) -> TelegramDiceView:
        """
        Creates a random dice view
        :param self:
        :param session:
        :param view_container:
        :return:
        """
        view_container = view_container if view_container is not None else session.view_container

        return TelegramDiceView(view_container)

    def get_user_from_update(self, update: telegram.Update):
        # Get the user that sent the message
        user = None
        if self.test:
            user = update.effective_user
        else:
            try:
                user = self.user_type.get_by_telegram_id(update.effective_user.id)
            except:
                print("Text received from a user that did not log in. Ignoring.")
        return user

    def check_stack(self, user, stack):
        # Create a stack if one doesn't exist yet. If this is the case, the bot is not expecting a message from
        # him, just return and ignore.
        if user not in stack:
            stack[user] = []
            print("Photo received from a user that the bot was not expecting a photo from. Ignoring.")
            return False
        # Check if the stack of the user is empty. If this is the case, the bot is not expecing a message from him,
        # just return and ignore.
        if len(stack[user]) == 0:
            print("Photo received from a user that the bot was not expecting a photo from. Ignoring.")
            return False
        return True

    def create_handlers(self):
        """
        Create handlers for receiving a text message and a button press. All messages and presses arrive here,
        and they are routed to the correct session and action.
        """

        def handle_photo_raw(update: telegram.Update, context: CallbackContext) -> None:
            """
            Handle a photo received from telegram
            :param update: update object from telegram
            :param context: context object from telegram
            """

            user = self.get_user_from_update(update)
            if user is None:
                return

            if not self.check_stack(user, self.user_photo_stacks):
                return

            # Pop the newest text listener and call it.
            photo: telegram.PhotoSize = update.message.photo[-1]
            file: telegram.File = photo.get_file()

            func, session = self.user_photo_stacks[user].pop(0)
            log_all_exceptions(
                lambda: func(session, file),
                session,
                self
            )

        @run_async
        def handle_photo_raw_async(update: telegram.Update, context: CallbackContext) -> None:
            handle_photo_raw(update, context)

        if self.test:
            self.dispatcher.add_handler(handle_photo_raw)
        else:
            photo_handler = MessageHandler(Filters.photo, handle_photo_raw_async)
            self.dispatcher.add_handler(photo_handler)

        def handle_text_raw(update: telegram.Update, context: CallbackContext) -> None:
            """
            Handle a text message received from telegram
            :param update: update object from telegram
            :param context: context object from telegram
            """

            user = self.get_user_from_update(update)
            if user is None:
                return

            if not self.check_stack(user, self.user_stacks):
                return

            # Pop the newest text listener and call it.

            func, session = self.user_stacks[user].pop(0)
            log_all_exceptions(
                lambda: func(session, update.message.text),
                session,
                self
            )

        @run_async
        def handle_text_raw_async(update: telegram.Update, context: CallbackContext) -> None:
            handle_text_raw(update, context)

        # Create a text message handler using this function and add it to the dispacher.
        if self.test:
            self.dispatcher.add_handler(handle_text_raw)
        else:
            text_handler = MessageHandler(Filters.text, handle_text_raw_async)
            self.dispatcher.add_handler(text_handler)

        def handle_document_raw(update: telegram.Update, context: CallbackContext) -> None:
            """
            Handle a document received from telegram
            :param update: update object from telegram
            :param context: context object from telegram
            """

            user = self.get_user_from_update(update)
            if user is None:
                return

            if not self.check_stack(user, self.user_document_stacks):
                return

            # Pop the newest text listener and call it.
            document: telegram.Document = update.message.document
            file: telegram.File = document.get_file()

            func, session = self.user_document_stacks[user].pop(0)
            log_all_exceptions(
                lambda: func(session, file),
                session,
                self
            )

        @run_async
        def handle_document_raw_async(update: telegram.Update, context: CallbackContext) -> None:
            handle_document_raw(update, context)

        if self.test:
            self.dispatcher.add_handler(handle_document_raw)
        else:
            document_handler = MessageHandler(Filters.document, handle_document_raw_async)
            self.dispatcher.add_handler(document_handler)

        def handle_button_raw(update: telegram.Update, context: CallbackContext) -> None:
            """
            Handle a button press received from telegram
            :param update: update object from telegram
            :param context: context object from telegram
            """
            try:
                user = self.get_user_from_update(update)
                if user is None:
                    return

                # Find the button id in the callback_query from telegram. This is the only data sent on the telegram
                # API.
                data = update.callback_query.data.split(';')
                if len(data) != 2:
                    BotLogger.error(
                        f" callback data is in incorrect format. Got: {data}, expected: '[session];[button]'. Ignoring.")
                    return
                session_id, button_id = data[0], data[1]

                # Locate the correct button and call it.
                session = None
                if user.id in Session.sessions and session_id in Session.sessions[user.id]:
                    session = Session.sessions[user.id][session_id]

                if session is None:
                    from bot_features.SystemFeatures.HierarchicalMenu.Code.hierarchical_menu import HierarchicalMenu
                    BotLogger.error("session no longer exists, ignoring.")
                    self.raw_bot.delete_message(user.telegram_id, update.effective_message.message_id)
                    HierarchicalMenu.run_menu(self, user)
                    return

                log_all_exceptions(
                    lambda: session.buttons[button_id].call_function(session),
                    session,
                    self
                )
            except Exception as e:
                BotLogger.error(f"Got exception when handling raw button click: {str(e)}")

        @run_async
        def handle_button_raw_async(update: telegram.Update, context: CallbackContext) -> None:
            handle_button_raw(update, context)

        # Create a button handler using this function and add it to the dispacher.
        if self.test:
            self.dispatcher.add_handler(handle_button_raw)
        else:
            button_handler = CallbackQueryHandler(handle_button_raw_async)
            self.dispatcher.add_handler(button_handler)
