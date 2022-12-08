from APIs.TalpiotAPIs import *
from APIs.TalpiotAPIs.Tasks.guarding.guarding_day import GuardingDay
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.session import Session
from bot_framework.ui.ui import UI


class TodayGuards(BotFeature):
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
        guarding_day: GuardingDay = GuardingDay.objects(date=datetime.date.today()).first()
        today_guards = set()
        for guarding_task in guarding_day.guardings:
            for guard in guarding_task.assignment:
                today_guards.add(guard.get_full_name())
        self.ui.summarize_and_close(session, [
            self.ui.create_text_view(session, "היום שומרים:\n\n" + '\n'.join(today_guards))
        ])

    def is_authorized(self, user: User) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        return "מתלם" in user.role
