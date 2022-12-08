from web_framework.server_side.infastructure.category import Category
from web_framework.server_side.infastructure.constants import *
from web_features.groups import matlam_edit, groups_edit, groups_admins, attendance_checks


class GroupsCategory(Category):
    def __init__(self):
        super().__init__(pages={
            'matlam_edit': matlam_edit.MatlamEdit,
            'groups_edit': groups_edit.GroupsEdit,
            'groups_admins': groups_admins.GroupsAdmins,
            'attendance_checkers': attendance_checks.AttendanceChecks,
        })

    def get_title(self) -> str:
        return "קבוצות"

    def is_authorized(self, user):
        return MATLAM in user.role
