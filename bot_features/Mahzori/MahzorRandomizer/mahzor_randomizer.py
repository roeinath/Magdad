from bot_framework import *
from APIs.ExternalAPIs import *
from APIs.TalpiotAPIs import *
import random
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.ui import UI

class MahzorRandomizer(BotFeature):

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)
        self.is_hantar_start = None
        self.all_user_text_view = None

    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """
        # check if the person that open the viduz is hantar to check if
        # he want to send message to everybody
        self.is_hantar_start = "חנתר" in session.user.role

        # if the hantar want to send everybody message it will hold here
        self.all_user_text_view = []

        # start talk with the user
        self.ui.create_text_view(session, "לכמה קבוצות לחלק?").draw()
        self.ui.get_text(session, self.got_number_from_user)

    def got_number_from_user(self, session: Session, str_number: str):
        """
        This function accept the num of groups and create them
        :param session: The normal session object
        :param str_number: The num of groups
        :return: None
        """
        self.ui.clear(session)

        if not self.check_valid_number_of_groups(str_number):
            self.ui.create_text_view(session, "אנא בחר מספר בין 2 ל10").draw()
            self.main(session)
            return

        number_of_groups = int(str_number)
        all_users_in_mahzor = UserConstraint.get_users_with_constraint(MachzorConstraint(session.user.mahzor))
        partitions = MahzorRandomizer.partition_list(all_users_in_mahzor, number_of_groups)

        # if the user is hantar then check if he want to send a message to everybody in which group they are
        # TODO schedule sending message
        if self.is_hantar_start:
            buttons = []
            buttons.append(self.ui.create_button_view("לשלוח הודעה לכל אחד באיזה קבוצה הוא",
                                                      lambda s: self.create_the_groups_text(s, number_of_groups,
                                                                                            partitions,
                                                                                            True)))
            buttons.append(self.ui.create_button_view("לא לשלוח הודעה לכל אחד באיזה קבוצה הוא",
                                                      lambda s: self.create_the_groups_text(s, number_of_groups,
                                                                                            partitions,
                                                                                            False)))
            self.ui.create_button_group_view(session, "מה ברצונך לעשות?", buttons).draw()

        # show only the user the groups
        else:
            self.create_the_groups_text(session, number_of_groups, partitions, False)

    def create_the_groups_text(self, session: Session, number_of_groups: int, partitions: [User], tell_users: bool):
        """
        This function create all the groups messages and send it to the user. after then he close the feature
        :param session: the normal session object
        :param number_of_groups: The num of groups
        :param partitions: The partitions of the users
        :param tell_users: True if we want to send to user in which group he is
        :return: None
        """
        messages: [View] = []
        for group in range(number_of_groups):
            messages.append(
                self.ui.create_text_view(session, self.create_group_text(group, partitions[group], tell_users)))


        # check if we need to send all the users in which group they are
        if tell_users:
            for text_view in self.all_user_text_view:
                text_view.draw()

        self.ui.summarize_and_close(session, messages)

    def create_group_text(self, group_num: int, group: [User], tell_users: bool):
        """
        This function create a one group message and if tell_users is true send a message to users in which grou they are
        :param group_num: The group num
        :param group: The users in the group
        :param tell_users: True if we want to tell each user in which group he is - only hantar can do it
        :return: one group message
        """
        group_text = f" חניכים בקבוצה מספר " + str(group_num + 1) + ":"
        for user in group:
            group_text += f"\n{user.name}"

            if tell_users:
                # send for each user in which group he his
                user_session = self.ui.create_session('mahzor_randomizer', user)
                self.all_user_text_view.append(
                    self.ui.create_text_view(user_session, "אתה בקבוצה מספר " + str(group_num + 1)))
        return group_text

    @staticmethod
    def partition_list(list_in, n):
        random.shuffle(list_in)
        return [list_in[i::n] for i in range(n)]

    def is_authorized(self, user: User) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        return "מתלם" in user.role

    def check_valid_number_of_groups(self, str_number: str):
        if not str_number.isdigit():
            return False

        number = int(str_number)
        if number < 2 or number > 10:
            return False

        return True
