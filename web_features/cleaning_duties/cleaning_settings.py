# from talpix import *
from APIs.TalpiotAPIs.CleaningTasks.cleaning.cleaning_week import CleaningWeek
from APIs.TalpiotAPIs.CleaningTasks.cleaning_task import CleaningTask
from web_features.cleaning_duties import permissions
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.constants import *


import datetime
from web_features.guardings.guarding_settings import GuardingSettings as options_layers
from APIs.TalpiotAPIs import User
from mongoengine import *

from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.datagrid import DataGrid
from web_framework.server_side.infastructure.components.form import Form
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel, VERTICAL, HORIZONTAL
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.page import Page



def delete_bad_cleanings():
    tasks = CleaningTask.objects

    used_tasks = []
    for w in CleaningWeek.objects:
        for d in w.days:
            used_tasks += d.cleaning_duties
    for t in tasks:
        if t not in used_tasks:
            t.delete()



def update_all_invites():
    for task in CleaningTask.objects(start_time__gte=datetime.date.today()):
        task.update_calendar_invite()
        task.save()



class DateSpan(Document):
    start = DateField()
    end = DateField()


class CleaningSettings(Page):
    def __init__(self, params):
        super().__init__()

        self.sp = None
        self.settings_grid = None
        
    def mark_interested(self, request):
        pass

    @staticmethod
    def get_title() -> str:
        return "הגדרת תורנויות"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_cleaning_task_admin(user)

    class GuardingSettingsForm(Document):
        not_guarding = ListField(ReferenceField(User))
        calendar_id = StringField()
    
    def delete_invites(self, date_span):
        with GoogleCalendar.get_instance() as gc:
            events = gc.get_events(CL_ID, datetime.datetime.combine(date_span.start, datetime.datetime.min.time()), datetime.datetime.combine(date_span.end, datetime.datetime.min.time()))
            for event in events:
                gc.delete_event('d9oga6q6ck59ir8i8r4omleqtg@group.calendar.google.com', event)

    def open_delete_invites(self):
        form = JsonSchemaForm(DateSpan, visible=['start', 'end'], display_name={
            'start': 'התחלה',
            'end': 'סיום',
        }, placeholder={
            'start': '0000-00-00',
            'end': '0000-00-00'
        },  submit= lambda x: self.delete_invites(x))

        self.popup = PopUp(form, title="יצירת שבוע", is_shown=True, is_cancelable=False)
        self.sp.add_component(self.popup)

    def delete_exemption(self, user):
        user.special_attributes['guarding_exemption'] = 0
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
        }, options_display= {
            'users': lambda x: "%d - %s" % (x.mahzor, str(x))
        },
        submit= lambda x: self.add_exemption_for_users(x, exemption_type))

        self.popup = PopUp(form, title="הוספת פטור שמירות", is_shown=True, is_cancelable=False)
        self.sp.add_component(self.popup)

    def show_information(self):
        self.sp.clear()


        # completely_exempt_users = []
        # night_exempt_users = []
        # for user in User.objects:
        #     if 'guarding_exemption' not in user.special_attributes:
        #         user.special_attributes['guarding_exemption'] = 0
        #     if user.special_attributes['guarding_exemption'] == 1:
        #         completely_exempt_users.append(user)
        #     if user.special_attributes['guarding_exemption'] == 2:
        #         night_exempt_users.append(user)
# 
        # print(completely_exempt_users)
        # print(night_exempt_users)
# 
        # self.sp.add_component(Label("פטורי שמירות גורפים"))
        # completely_exempt_table = GridPanel(len(completely_exempt_users), 2)
        # i = 0
        # for u in completely_exempt_users:
        #     completely_exempt_table.add_component(Label(u.name), i, 0)
        #     completely_exempt_table.add_component(Button("הסר", lambda u=u: self.delete_exemption(u)), i, 1)
        #     i+=1
        # self.sp.add_component(completely_exempt_table)
# 
        # self.sp.add_component(Label("פטורי שמירות לילה"))
        # night_exempt_table = GridPanel(len(night_exempt_users), 2)
        # i = 0
        # for u in night_exempt_users:
        #     night_exempt_table.add_component(Label(u.name), i, 0)
        #     night_exempt_table.add_component(Button("הסר", lambda u=u: self.delete_exemption(u)), i, 1)
        #     i+=1
        # self.sp.add_component(night_exempt_table)
        #     
        # self.sp.add_component(Button("הוסף פטור שמירות גורף", lambda: self.open_add_exemption_form(1)))
        # self.sp.add_component(Button("הוסף פטור שמירות לילה", lambda: self.open_add_exemption_form(2)))

        self.sp.add_component(Button("מחק תורנויות לא הגיוניות (לאדמינים)", delete_bad_cleanings))
        # self.sp.add_component(Button("מחק זימוני קאלנדר", self.open_delete_invites))
        # self.sp.add_component(Button("עדכן את כל זימוני הקאלנדר", update_all_invites))

        print("done")

    def get_page_ui(self, user):
        self.sp = StackPanel([])

        self.show_information()

        return self.sp