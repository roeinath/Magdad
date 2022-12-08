# from general import *

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.Group.group import Group
from APIs.TalpiotAPIs.AttendanceChecker.scheduled_attendance_checker import ScheduledAttendanceChecker
from web_features.groups.permissions import is_user_admin
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_framework.server_side.infastructure.components.confirmation_button import ConfirmationButton
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page


class AttendanceChecks(Page):
    @staticmethod
    def get_title() -> str:
        return "וידוא נוכחות"

    def __init__(self, params):
        super().__init__()
        self.sp: StackPanel = None
        self.user = None

    def get_page_ui(self, user):
        self.sp = StackPanel([])
        self.user = user
        self.draw()
        return self.sp

    def draw(self):
        self.sp.clear()

        self.sp.add_component(Label('וידו"צים עתידיים', size=SIZE_EXTRA_LARGE))
        groups = Group.objects(admins=self.user) if not self.user.bot_admin else Group.objects()
        scheduled_checkers = ScheduledAttendanceChecker.objects(group__in=groups)
        accordion = Accordion(
            [self.get_vidutz_table(x) for x in scheduled_checkers],
            [x.name for x in scheduled_checkers]
        )
        self.sp.add_component(accordion)

    def get_vidutz_table(self, scheduled_checker: ScheduledAttendanceChecker):
        gp = GridPanel(len(scheduled_checker.missings) + 1, 2)
        titles = ["שם", "סיבה"]
        for i in range(len(titles)):
            gp.add_component(Label(titles[i], fg_color='white'), 0, i, bg_color=COLOR_PRIMARY_DARK)
        for i, missing_reason in enumerate(scheduled_checker.missings):
            gp.add_component(Label(missing_reason.user.get_full_name()), i + 1, 0)
            gp.add_component(Label(missing_reason.reason), i + 1, 1)
        return StackPanel([
            Label(f"קבוצה: {scheduled_checker.group.name}"),
            Label(f"סה\"כ חסרים: {len(scheduled_checker.missings)}"),
            gp,
            ConfirmationButton('מחיקת וידו"צ', lambda: scheduled_checker.delete(), bg_color='red')
        ])
