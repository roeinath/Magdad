from typing import List, Tuple

from APIs.TalpiotAPIs.AttendanceChecker.scheduled_attendance_checker import ScheduledAttendanceChecker
from APIs.TalpiotAPIs.AttendanceChecker.state import State
from APIs.TalpiotAPIs.Group import CommandedGroup
from bot_features.TalpiotGeneral.AttendenceChecker.Code.logic.attendance_cadet_data import AttendanceCadetData

from bot_framework.session import Session


class AttendanceData:
    def __init__(self, name: str, user_manager, admin_manager, scheduled_checker: ScheduledAttendanceChecker = None):
        """
        Create a new VidutzData instance to manage a single vidutz
        :param founder_session: Session object of initiating hantar
        """
        self.name: str = name
        self.members: List[AttendanceCadetData] = list()
        self.admins: List[AttendanceCadetData] = list()

        self.user_manager = user_manager
        self.admin_manager = admin_manager

        self.closed = False

        self.scheduled_checker = scheduled_checker

    def add_member_session(self, member_session: Session, state: State) -> None:
        """
        Add a hapash to the vidutz's cadet list
        :param hapash_session: Session object of added hapash
        """
        new_data = AttendanceCadetData(member_session, None, state=state)
        self.members.append(new_data)

    def add_admin_session(self, admin_session: Session, state: State) -> None:
        """
        Add a hantar to the vidutz's cadet list
        :param hantar_session: Session object of added hantar
        :param state: Default state for this hantar (usually HERE for initiator and OMW otherwise)
        """
        new_data = AttendanceCadetData(admin_session, None, state=state)
        self.admins.append(new_data)

    def update_all_views(self):
        for admin in self.admins:
            self.admin_manager.update_view(admin)
        for user in self.members:
            if user in self.admins:
                continue  # ignore users that are admins, because their views were already updated in the previous step
            self.user_manager.update_view(user)

    def get_all_members(self):
        return self.members + self.admins

    def sort(self) -> None:
        """
        Sorts the children lists by state and name
        """
        self.members.sort(key=AttendanceData.key_func)

    def get_summary(self, commanded_group: CommandedGroup = None) -> str:
        """
        Generates the vidutz's state summary in string format, to be left when the vidutz ends.
        :return: The summary.
        """
        group_name = commanded_group.name if commanded_group is not None else ''
        summary = f"סיכום וידוא צוערים עבור {self.name}\n" \
                  f"{group_name}\n" \
                  f"---------------------\n\n"

        members_of_group = self.members
        if commanded_group is not None:
            members_of_group = [user for user in self.members if user.session.user in commanded_group.participants]

        num_present = 0
        for m in members_of_group:
            if m.state == State.HERE:
                num_present += 1
        summary += f"נכחו: {num_present}\n\n"

        didnt_mark = []
        missing_no_reason = []
        missing_reasons = []

        for member in members_of_group:
            if member.state == State.HERE:
                continue

            missing_reason = None
            if self.scheduled_checker is not None:
                missing_reason = self.scheduled_checker.get_missing_reason_if_exists(member.session.user)

            if missing_reason is not None:
                missing_reasons.append((member.session.user, missing_reason))
            else:
                if member.state == State.OMW:
                    didnt_mark.append(member.session.user)
                if member.state == State.NO:
                    missing_no_reason.append(member.session.user)

        summary += "לא סימנו נוכחות:\n"
        for u in didnt_mark:
            summary += f"{u.name}\n"

        summary += "\nלא נכחו אך לא ציינו סיבה:\n"
        for u in missing_no_reason:
            summary += f"{u.name}\n"

        summary += "\nשאר הצוערים: \n"
        for u, reason in missing_reasons:
            summary += f"{u.name} - {reason}\n"

        return summary

    @staticmethod
    def key_func(acd: AttendanceCadetData) -> Tuple[State, str]:
        """
        Helper function - used as key function for sorting.
        :param acd: A cadet
        :return: A tuple of (cadet's state, cadet's name)
        """
        return -acd.state.value, acd.session.user.name
