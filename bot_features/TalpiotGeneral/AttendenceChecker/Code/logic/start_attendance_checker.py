from APIs.TalpiotAPIs.AttendanceChecker.scheduled_attendance_checker import ScheduledAttendanceChecker
from APIs.TalpiotAPIs.Group.group import Group

from bot_features.TalpiotGeneral.AttendenceChecker.Code.logic.attendance_data import AttendanceData
from bot_features.TalpiotGeneral.AttendenceChecker.Code.ui.attendance_checker_admin import AttendanceCheckerAdmin
from bot_features.TalpiotGeneral.AttendenceChecker.Code.ui.attendance_checker_user import AttendanceCheckerUser
from bot_framework.ui.ui import UI


def start_checking(ui: UI, group: Group, name: str, scheduled_checker: ScheduledAttendanceChecker = None) -> None:
    data = AttendanceData(name, AttendanceCheckerUser(ui), AttendanceCheckerAdmin(ui), scheduled_checker)
    for user in group.participants:
        data.user_manager.start_user_checker(data, user)
    for user in group.admins:
        data.admin_manager.start_admin_checker(data, user)
    data.update_all_views()
