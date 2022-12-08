from bot_framework import View
from bot_framework.ui.ui import UI
from bot_framework.session import Session
from bot_framework.Feature.bot_feature import BotFeature
from APIs.ExternalAPIs import ScheduledJob
from APIs.TalpiotAPIs import User, SecretCodeManager


class Start(BotFeature):

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
        if 'secret_code' not in session.data:
            return

        secret_code = session.data['secret_code']
        users = User.objects.filter(secret_code=secret_code)
        if not (len(users) > 0):
            print("No user with that secret code.")
            self.ui.summarize_and_close(session, [self.ui.create_text_view(session, "קוד סודי לא נכון, פנה לרמד talpix")])
            return

        user: User = users[0]
        user.telegram_id = session.data['telegram_id']
        user.secret_code = SecretCodeManager.generate_code()
        user.save()

        session.feature_name = "start"
        session.user = user
        self.ui.summarize_and_close(session, [
            self.ui.create_text_view(session, f"Welcome {user.name}!\nYou can now use the system.")])

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
