import datetime
from typing import List

from APIs.ExternalAPIs import CalendarEvent
from APIs.TalpiotAPIs.AttendanceChecker.missing_reason import MissingReason
from APIs.TalpiotAPIs.AttendanceChecker.scheduled_attendance_checker import ScheduledAttendanceChecker
from APIs.TalpiotAPIs.Group import *
from APIs.TalpiotAPIs.User.user import User
from bot_features.SystemFeatures.HierarchicalMenu.Code.hierarchical_menu import HierarchicalMenu
from bot_features.TalpiotGeneral.AttendenceChecker.Code.logic.start_attendance_checker import start_checking
from bot_features.TalpiotGeneral.AttendenceChecker.Code.ui.attendance_checker_init import AttendanceCheckerInit
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.button import Button
from bot_framework.ui.ui import UI

RELEVANT_CHANGED_ATTRIBUTES = {'title', 'start_time', 'non_users_attendees', 'creator', 'description'}


class AttendanceChecker(BotFeature):
    calendar_id = "joo4rvfdjb479v7enspbqnfj7c@group.calendar.google.com"

    def __init__(self, ui: UI):
        """
        Create a new vidutz module instance
        :param ui: UI instance to be used
        """
        super().__init__(ui)

    def main(self, session: Session) -> None:
        buttons = [
            Button("פתיחת/תכנון וידוא נוכחות חדש", AttendanceCheckerInit(self).main),
            Button("פתיחת וידוא נוכחות מתוכנן", self.select_open_event),
            Button("דיווח על חיסור מלוז", self.select_missing_event),
            Button("חזרה לתפריט הראשי 🔙", self.return_to_menu)
        ]
        self.ui.create_button_group_view(session, "מה ברצונך לעשות?", buttons).draw()

    def calendar_event_parser(self, calendar_event_id, changed_attributes: dict = None, is_deleted: bool = False):
        event: CalendarEvent = CalendarEvent.objects(calendar_event_id=calendar_event_id).first()
        if event is None:
            print("Event not found")
            return
        relevant_changes = RELEVANT_CHANGED_ATTRIBUTES.intersection(set(changed_attributes.keys()))
        if changed_attributes and not relevant_changes:
            return
        event_creator = event.creator or User.objects(name="יהלי אקשטיין").first()
        session = Session(self.get_feature_name(), event_creator, self.ui)

        event.description = event.description or ''
        group_names = [line.strip() for line in event.description.split('\n')]

        selected_groups_description = set(Group.objects(name__in=group_names))

        group_mails = [email for email in event.non_users_attendees]
        selected_groups_mails = set(Group.objects(calendar_id__in=group_mails))
        selected_groups = selected_groups_description.union(selected_groups_mails)

        if not selected_groups:
            self.ui.create_text_view(session, f"עבור האירוע - {event.title}\n"
                                              f"לא נמצאה קבוצה מתאימה - {event.description} 😔\n"
                                              f"ייתכן ואין לך הרשאות לקבוצה או שלא כתבת בתיאור האירוע את השם המדויק").draw()

        for selected_group in selected_groups:
            for checker in ScheduledAttendanceChecker.objects(event_id=calendar_event_id):
                checker.delete()
            if is_deleted:
                continue

            scheduled_checker = ScheduledAttendanceChecker(name=event.title, group=selected_group, missings=[],
                                                           event_id=calendar_event_id).save()
            vidutz_time = event.start_time - datetime.timedelta(minutes=10)
            self.schedule_job(vidutz_time, checker_id=scheduled_checker.id)
            self.ui.create_text_view(session, f"עבור האירוע - {event.title}\n"
                                              f"וידוא נוכחות מתוכנן לקבוצה 👥 - {selected_group.name}\n"
                                              f"הוידו\"צ יתחיל בשעה ⏰ {vidutz_time}").draw()

    def select_open_event(self, session: Session):
        buttons = []
        groups = Group.objects(admins=session.user)
        for e in ScheduledAttendanceChecker.objects(group__in=groups):
            buttons.append(Button(e.name, lambda s, e=e: self.start_scheduled_checker(e)))
        buttons.append(Button("חזרה 🔙", self.main))
        if len(buttons) == 0:
            self.ui.create_text_view(session, "אין לוזים מתוכננים").draw()
        else:
            self.ui.create_button_group_view(session, "איזה וידוא נוכחות את/ה רוצה לפתוח? ", buttons).draw()

    def select_missing_event(self, session: Session):
        def event_selected(session: Session, event: ScheduledAttendanceChecker):
            session.selected_event = event
            self.give_missing_reason(session)

        buttons = []
        groups = Group.objects(participants=session.user)
        for e in ScheduledAttendanceChecker.objects(group__in=groups):
            if any(m.user == session.user for m in e.missings):
                continue
            buttons.append(Button(e.name, lambda s, e=e: event_selected(s, e)))

        if len(buttons) == 0:
            self.ui.create_text_view(session, "אין לוזים מתוכננים").draw()
        else:
            buttons.append(Button("חזרה לתפריט הראשי 🔙", self.return_to_menu))
            self.ui.create_button_group_view(session, "לאיזה לוז לא תגיע/י?", buttons).draw()

    def give_missing_reason(self, session: Session):
        def reason_given(session: Session, reason: str):
            r = MissingReason(user=session.user, reason=reason)
            r.save()
            session.selected_event.missings.append(r)
            session.selected_event.save()
            self.select_missing_event(session)

        self.ui.create_text_view(session, "מה סיבת החיסור?").draw()
        self.ui.get_text(session, reason_given)

    def return_to_menu(self, session: Session):
        self.ui.clear(session)
        HierarchicalMenu.run_menu(self.ui, session.user)

    def get_summarize_views(self, session: Session) -> List[View]:
        return list()

    def is_authorized(self, user: User) -> bool:
        return True

    def get_command(self) -> str:
        return "attendance"

    def start_scheduled_checker(self, checker):
        print("Starting scheduled attendance checker for " + checker.name + "...")
        checker.delete()
        start_checking(self.ui, checker.group, checker.name, checker)

    def scheduled_jobs_parser(self, checker_id):
        checker = None
        try:
            checker = ScheduledAttendanceChecker.objects(id=checker_id)[0]
        except:
            print(
                "Scheduled attendance skipped because the corresponding info object was deleted. Probably was started manually. This is normal and can be ignored.")

        if checker is not None:
            self.start_scheduled_checker(checker)
