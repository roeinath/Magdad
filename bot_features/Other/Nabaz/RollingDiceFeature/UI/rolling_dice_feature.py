from bot_framework import *
from APIs.ExternalAPIs import *
from APIs.TalpiotAPIs import *
from APIs.Database import *
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.ui import UI
MAX_NUM_OF_DICE = 4
MIN_NUM_OF_DICE = 1


class RollingDiceFeature(BotFeature):

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
        self.ui.create_text_view(session, "כמה קוביות לזרוק? " + f"({MIN_NUM_OF_DICE}-{MAX_NUM_OF_DICE})").draw()
        self.ui.get_text(session, self.got_num_of_dice)

    def got_num_of_dice(self, session: Session, num: str):
        if not num.isdigit() or int(num) < MIN_NUM_OF_DICE or int(num) > MAX_NUM_OF_DICE:
            self.main(session)
            return

        views = [self.ui.create_dice_view(session) for i in range(int(num))]
        self.ui.summarize_and_close(session, views)

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
