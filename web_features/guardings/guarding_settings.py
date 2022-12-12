# from general import *
import datetime
import time
from mongoengine import *
from mongoengine.document import Document
from mongoengine.fields import DateField, ListField

from APIs.ExternalAPIs import GoogleCalendar
from APIs.ExternalAPIs.GoogleCalendar.calendar_invite_creator import delete_invite_from_calendar, \
    get_invites_by_date_span, GUARDING_CALENDAR_ID
from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.Tasks.guarding.guarding_week import GuardingWeek
from APIs.TalpiotAPIs.Tasks.task import Task
from web_features.guardings import permissions
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.page import Page
from web_features.guardings.guarding_constants import *


def delete_bad_guardings():
    tasks = Task.objects

    used_tasks = []
    for w in GuardingWeek.objects:
        for d in w.days:
            used_tasks += d.guardings
    for t in tasks:
        if t not in used_tasks:
            t.delete()


def update_all_invites():
    for task in Task.objects(start_time__gte=datetime.date.today()):
        task.update_calendar_invite(send_updates='none')
        task.save()


class GuardingSettings(Page):
    def __init__(self, params):
        super().__init__()

        self.sp = None
        self.settings_grid = None
        self.user = None

    def mark_interested(self, request):
        pass

    @staticmethod
    def get_title() -> str:
        return "הגדרת שמירות"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_guarding_admin(user)

    class GuardingSettingsForm(Document):
        not_guarding = ListField(ReferenceField(User))
        calendar_id = StringField()

    def delete_invites(self, date_span):
        for event in get_invites_by_date_span(GUARDING_CALENDAR_ID, date_span):
            if date_span.only_empty and len(event.attendees) > 0:
                continue
            delete_invite_from_calendar(GUARDING_CALENDAR_ID, event, 'none')
            print(f"Event {event.calendar_event_id} deleted")
            time.sleep(0.05)

    def open_delete_invites(self):
        class DateSpan(Document):
            start = DateField()
            end = DateField()
            only_empty: bool = BooleanField()

        form = JsonSchemaForm(DateSpan, visible=['start', 'end', 'only_empty'], display_name={
            'start': 'התחלה',
            'end': 'סיום',
            'only_empty': 'רק זימונים ריקים (ללא שומרים)',
        }, placeholder={
            'start': '0000-00-00',
            'end': '0000-00-00'
        }, submit=lambda x: self.delete_invites(x))

        self.popup = PopUp(form, title="יצירת שבוע", is_shown=True, is_cancelable=False)
        self.sp.add_component(self.popup)

    def delete_exemption(self, user):
        user.special_attributes['guarding_exemption'] = GUARDING_EXEMPTION_NONE
        user.save()
        self.show_information()

    def add_exemption_for_users(self, form_answer, exemption_type):
        for user in form_answer.users:
            user.special_attributes['guarding_exemption'] = exemption_type
            user.save()
        self.show_information()

    def open_add_exemption_form(self, exemption_type):

        class ExemptionFormAnswer(Document):
            users = ListField(ReferenceField(User))

        form = JsonSchemaForm(ExemptionFormAnswer, visible=['users'], display_name={
            'users': 'חניכים',
        }, placeholder={
            'users': '[]',
        }, options={
            'users': User.objects,
        }, options_display={
            'users': lambda x: "%d - %s" % (x.mahzor, str(x))
        },
                              submit=lambda x: self.add_exemption_for_users(x, exemption_type))

        self.popup = PopUp(form, title="הוספת פטור שמירות", is_shown=True, is_cancelable=False)
        self.sp.add_component(self.popup)

    def show_information(self):
        self.sp.clear()

        completely_exempt_users = []
        night_exempt_users = []
        for user in User.objects:
            if 'guarding_exemption' not in user.special_attributes:
                user.special_attributes['guarding_exemption'] = GUARDING_EXEMPTION_NONE
            if user.special_attributes['guarding_exemption'] == GUARDING_EXEMPTION_TOTAL:
                completely_exempt_users.append(user)
            if user.special_attributes['guarding_exemption'] == GUARDING_EXEMPTION_NIGHT:
                night_exempt_users.append(user)

        print(completely_exempt_users)
        print(night_exempt_users)

        if permissions.is_user_guarding_super_admin(self.user):
            self.sp.add_component(Label("פטורי שמירות גורפים"))
            completely_exempt_table = GridPanel(len(completely_exempt_users), 2)
            i = 0
            for u in completely_exempt_users:
                completely_exempt_table.add_component(Label(u.name), i, 0)
                completely_exempt_table.add_component(Button("הסר", lambda u=u: self.delete_exemption(u)), i, 1)
                i += 1
            self.sp.add_component(completely_exempt_table)

            self.sp.add_component(Label("פטורי שמירות לילה"))
            night_exempt_table = GridPanel(len(night_exempt_users), 2)
            i = 0
            for u in night_exempt_users:
                night_exempt_table.add_component(Label(u.name), i, 0)
                night_exempt_table.add_component(Button("הסר", lambda u=u: self.delete_exemption(u)), i, 1)
                i += 1
            self.sp.add_component(night_exempt_table)

            self.sp.add_component(Button("הוסף פטור שמירות גורף", lambda: self.open_add_exemption_form(1)))
            self.sp.add_component(Button("הוסף פטור שמירות לילה", lambda: self.open_add_exemption_form(2)))

        self.sp.add_component(Button("מחק שמירות לא הגיוניות (לאדמינים)", delete_bad_guardings))
        self.sp.add_component(Button("מחק זימוני קאלנדר", self.open_delete_invites))
        self.sp.add_component(Button("עדכן את כל זימוני הקאלנדר החל מהיום", update_all_invites))

        print("done")

    def get_page_ui(self, user):
        self.sp = StackPanel([])

        self.user = user
        self.show_information()

        return self.sp
