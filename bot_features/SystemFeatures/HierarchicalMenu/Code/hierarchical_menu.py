from __future__ import annotations
import os
from APIs.ExternalAPIs import ScheduledJob
from APIs.TalpiotSystem import TBLogger
from APIs.TalpiotAPIs import User
from bot_features.SystemFeatures.HierarchicalMenu.Code.menu_node import MenuNode
from bot_framework.Feature.FeatureSettings import FeatureType
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.crash_logger import log_all_exceptions
from bot_framework.session import Session
from bot_framework.ui.button import Button
from bot_framework.ui.ui import UI

FEATURES_HOME_DIR = os.path.abspath('bot_features')
SESSION_VAR_LAST_VIEW = "last_view"


class HierarchicalMenu(BotFeature):
    """
    This menu will analyze the hierarchical structure of the Features directory,
    and present it to the user.
    """
    __instance = None

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        if HierarchicalMenu.__instance is not None:
            raise Exception("This class is a singleton!")

        HierarchicalMenu.__instance = self
        super().__init__(ui)
        self.root_node: MenuNode = MenuNode(os.path.abspath(FEATURES_HOME_DIR), parent=None, ui=ui)

    @staticmethod
    def get_instance(ui: UI):
        if HierarchicalMenu.__instance is None:
            HierarchicalMenu(ui)
        return HierarchicalMenu.__instance

    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """
        self.ui.clear(session)
        self.show_menu(session, self.root_node)

    def show_menu(self, session: Session, node: MenuNode):
        """
        Show the menu for a given session and a node.
        :param session: The session to show the menu for
        :param node: The node to present
        :return:
        """
        # breakpoint()
        buttons = self.get_buttons(session, node)

        buttons = sorted(buttons, key=lambda button: button.title)

        if len(buttons) == 0:
            self.ui.create_text_view(session, "הפיצ׳רים בקטגוריה זו עדיין בבנייה או שאין לך הרשאות לצפות בהם.").draw()

        if node.parent is not None:
            buttons.append(
                self.ui.create_button_view("🔙", lambda new_session: self.show_menu(new_session, node.parent))
            )

        new_message = self.ui.create_button_group_view(session, "תפריט " + node.display_name + ":", buttons)
        if SESSION_VAR_LAST_VIEW not in session.data:
            new_message.draw()
            session.data[SESSION_VAR_LAST_VIEW] = new_message
        else:
            session.data[SESSION_VAR_LAST_VIEW].update(new_message.text, new_message.buttons)

    def get_buttons(self, session: Session, node: MenuNode) -> [Button]:
        """
        Returns the button for the given Node.
        :param session: The session to get for
        :param node: The MenuNode to get from
        :return:
        """
        buttons = []

        for inner_node in node.payload:
            if not inner_node.show_in_menu:
                continue
            button_title = inner_node.display_name
            if inner_node.type == FeatureType.REGULAR_FEATURE:
                button_title = inner_node.emoji + ' ' + button_title
                object: BotFeature = inner_node.payload
                if not object.is_authorized(session.user):
                    continue
                button_action = lambda _session, _object=object: self.run_feature(_session, _object)

            elif inner_node.type == FeatureType.FEATURE_CATEGORY:
                button_title = "🗂 " + button_title
                button_action = lambda _session, _inner_node=inner_node: self.show_menu(_session, _inner_node)

            buttons.append(self.ui.create_button_view(title=button_title, callback=button_action))

        return buttons

    def run_feature(self, session: Session, feature_object: BotFeature):
        """
        Starts a given feature to the given session. Ensure
        no other instances of this features is ran
        :param session:
        :param feature_object:
        :return:
        """
        self.ui.clear(session)

        TBLogger.info(f"Running feature: {str(feature_object.__class__)}")

        self.ui.clear_feature_sessions_user(str(feature_object.__class__.__name__), session.user)
        new_session = self.ui.create_session(str(feature_object.__class__.__name__), session.user)
        Session.delete_session(session)

        log_all_exceptions(
            lambda: feature_object.main(new_session),
            new_session,
            self.ui
        )

    def get_summarize_views(self, session: Session) -> [View]:
        """
        Called externally when the BotManager wants to close this feature.
        This function returns an array of views that summarize the current
        status of the session. The array can be empty.
        :param session: Session object
        :return: Array of views summarizing the current feature Status.
        """
        pass

    def is_authorized(self, user: User) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        return "מתלם" in user.role

    def get_scheduled_jobs(self) -> [ScheduledJob]:
        """
        Get jobs (scheduled functions) that need to be called at specific times.
        :return: List of Jobs that will be created and called.
        """
        return []

    @staticmethod
    def run_menu(ui: UI, user: User):
        """
        Starts the menu, ensures that no other menu
        is running currently
        :param ui: The UI to start on
        :param user: The user to send to
        :return:
        """
        ui.clear_feature_sessions_user("list", user)
        session = ui.create_session("list", user)

        feature = HierarchicalMenu.get_instance(ui)

        log_all_exceptions(
            lambda: feature.main(session),
            session,
            ui
        )


def test_this():
    global FEATURES_HOME_DIR
    FEATURES_HOME_DIR = "../../../"
    h = HierarchicalMenu.get_instance(None)


if __name__ == '__main__':
    test_this()
