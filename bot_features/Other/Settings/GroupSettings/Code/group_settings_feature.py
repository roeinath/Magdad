from bot_framework import *
from APIs.ExternalAPIs import *
from APIs.TalpiotAPIs import *
from APIs.Database import *
from APIs.TalpiotAPIs import get_user_groups
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.ui import UI

class GroupSettings(BotFeature):

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)

    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """
        my_groups = get_user_groups(user=session.user)
        self.show_groups(session, my_groups)

    def show_groups(self, session: Session, groups: [Group]):
        buttons = [
            self.ui.create_button_view(
                group.name,
                lambda _session, _group=group: self.show_group(_session, _group)
            ) for group in groups
        ]
        buttons.append(self.ui.create_button_view("יציאה", lambda s: self.ui.summarize_and_close(s)))
        self.ui.create_button_group_view(session, title="הקבוצות שלך:", buttons=buttons).draw()

    def show_group(self, session: Session, group: Group):
        self.ui.summarize_and_close(
            session,
            [
                self.ui.create_text_list_view(
                    session,
                    title="מציג את קבוצה: " + group.name,
                    list_items=[user.name for user in group.participants]
                )
            ]
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
