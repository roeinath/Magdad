import datetime

from APIs.TalpiotAPIs.AttendanceChecker.scheduled_attendance_checker import ScheduledAttendanceChecker
from APIs.TalpiotAPIs.Group import *
from bot_features.TalpiotGeneral.AttendenceChecker.Code.logic.start_attendance_checker import start_checking
from bot_framework.session import Session
from bot_framework.ui.button import Button


class AttendanceCheckerInit(object):
    def __init__(self, owner_feature):
        self.owner_feature = owner_feature

    def main(self, session: Session) -> None:
        def group_selected(session, group):
            session.selected_group = group
            self.select_name(session)

        self.owner_feature.ui.clear(session)
        self.owner_feature.ui.create_text_view(session, "טוען קבוצות...").draw()

        buttons = []
        for group in Group.objects(admins=session.user):
            buttons.append(Button(group.name, lambda session, group=group: group_selected(session, group)))
        buttons.append(Button("ביטול", self.owner_feature.ui.clear))

        self.owner_feature.ui.clear(session)
        self.owner_feature.ui.create_button_group_view(session, "בחר קבוצה", buttons).draw()

    def select_name(self, session: Session) -> None:
        def name_selected(session, name):
            session.selected_name = name
            self.select_immediate_or_timed(session)

        self.owner_feature.ui.create_text_view(session, "איך לקרוא לוידוא?").draw()
        self.owner_feature.ui.get_text(session, name_selected)

    def select_immediate_or_timed(self, session: Session) -> None:
        def now_callback(session: Session):
            self.owner_feature.ui.clear(session)
            start_checking(self.owner_feature.ui, session.selected_group, session.selected_name)

        buttons = [
            Button("עכשיו", now_callback),
            Button("מאוחר יותר", self.select_date)
        ]
        self.owner_feature.ui.create_button_group_view(session, "מתי לפתוח וידוא נוכחות?", buttons).draw()

    def select_date(self, session: Session) -> None:
        def date_selected(_, session, date):
            session.selected_date = date
            self.select_time(session)

        self.owner_feature.ui.create_date_choose_view(session, date_selected, title="באיזה יום?").draw()

    def select_time(self, session: Session) -> None:
        def time_selected(_, session, time):
            session.selected_time = time
            self.schedule_checker(session.selected_name, session.selected_group, session.selected_date,
                                  session.selected_time)
            self.owner_feature.ui.clear(session)
            self.owner_feature.ui.create_text_view(session, "האירוע תוכנן").draw()

        self.owner_feature.ui.create_time_choose_view(session, time_selected).draw()

    def schedule_checker(self, name: str, group: Group, date: datetime.date, time: datetime.datetime):
        scheduled_checker = ScheduledAttendanceChecker(name=name, group=group, missings=[])
        scheduled_checker.save()
        self.owner_feature.schedule_job(datetime.datetime.combine(date, time.time()), checker_id=scheduled_checker.id)
