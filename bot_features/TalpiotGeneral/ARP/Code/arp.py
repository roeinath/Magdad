from typing import List

from bot_framework.Activity.closest_name_activity import ClosestNameActivity
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.ui import UI, Button
from APIs.TalpiotAPIs.User.user import User


class ARP(BotFeature):

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)

    # This is the first function that run when user press to to start the feature
    def main(self, session: Session) -> None:
        self.ui.create_text_view(session, "את מי לחפש?").draw()

        # wait to text from the user - the second argument is the function we call
        # after we accept a text from the user - if we want to pass also arguments we will use lambda
        # an example for that is in line 33
        self.ui.get_text(session, self.got_name_from_user)

    def got_name_from_user(self, session: Session, name: str) -> None:
        users = User.objects

        data = {}
        for user in users:
            data[user.name] = user

        def try_again(s: Session) -> None:
            """
            This function call after the user press the try again button
            :return: None
            """
            self.ui.clear(s)
            self.main(s)

        self.ui.create_closest_name_view(session, data, name, 5, lambda s, c, u: self.button_pressed(s, c, u), try_again).draw()

    def button_pressed(self, session: Session, closest_activity: ClosestNameActivity, user: User) -> None:
        """
        This function call after
        :param session: Like always
        :param user: The user object that the user press
        :return: None
        """

        self.ui.clear(session)
        self.ui.summarize_and_close(session, [self.ui.create_contact_view(session, user.name, user.phone_number, user.email)])

    def get_command(self) -> str:
        """
        :return: The string tha invoke this feature
        """
        return "arp"

    def get_summarize_views(self, session: Session) -> [View]:
        return []

    def is_authorized(self, user: User) -> bool:
        return "מתלם" in user.role

