import datetime

from mongoengine.document import Document
from mongoengine.fields import StringField, DateField
from mongoengine.queryset.visitor import Q

import web_features.shagmach.permissions as permissions
from web_framework.server_side.infastructure.constants import *
from APIs.TalpiotAPIs.Shagmach.computer_fix_request import FixTypes
from web_features.shagmach.rasaput_utils import *
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanelColumn, \
    DocumentGridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page


class ComputerErrors(Page):
    @staticmethod
    def get_title() -> str:
        return "תקלות מחשוב"

    def report(self):
        pass

    def __init__(self, params):
        super().__init__()
        self.sp = StackPanel([])

        self.container_table = None
        self.popup = None
        self.reports_stack = StackPanel([])
        self.closed_reports_stack = StackPanel([])

    def get_page_ui(self, user):
        self.user = user

        self.sp.add_component(Label("הצגת תקלות מחשוב", size=SIZE_EXTRA_LARGE))
        self.sp.add_component(Button("דווח/י על תקלת מחשוב", self.create_request))

        self.sp.add_component(
            Label(f"{len(ComputerFixRequest2.objects(Q(closed=False) | Q(closed=None)))} תקלות פתוחות",
                  size=SIZE_LARGE))
        self.sp.add_component(Divider())
        self.sp.add_component(self.reports_stack)

        self.sp.add_component(Label(f"{len(ComputerFixRequest2.objects(closed=True))} תקלות סגורות", size=SIZE_LARGE))
        self.sp.add_component(Divider())
        self.sp.add_component(self.closed_reports_stack)

        self.draw_tables()

        return self.sp

    def draw_tables(self):
        self.reports_stack.clear()
        self.reports_stack.add_component(self.get_reports_table(is_closed=False))
        self.closed_reports_stack.clear()
        self.closed_reports_stack.add_component(self.get_reports_table(is_closed=True))

    def get_reports_table(self, is_closed):
        reports_table = DocumentGridPanel(
            ComputerFixRequest2,
            column_list=[
                DocumentGridPanelColumn('user', "שם",
                                        component_parser=lambda request, user: Label(f"{user.name} - {user.mahzor}")),
                DocumentGridPanelColumn('computer_id', "מזהה מחשב"),
                DocumentGridPanelColumn('user', "מספר טלפון",
                                        component_parser=lambda request, user: Label(user.phone_number)),
                DocumentGridPanelColumn('fix_type', "סוג תקלה"),
                DocumentGridPanelColumn('description', "תיאור התקלה"),
                DocumentGridPanelColumn('is_computer_in_tamam', "האם המחשב הובא ליחידה?", self.is_in_tamam_component),
                DocumentGridPanelColumn('is_computer_working', "האם המחשב עובד?"),
                DocumentGridPanelColumn('computer_serial', "סיריאלי"),
                DocumentGridPanelColumn('finish_deadline', "דדליין סיום", self.deadline_component),
                DocumentGridPanelColumn('statuses', "סטטוס", self.statuses_component),
            ], filter_by={'closed': is_closed}
        )
        reports_table.add_column(self.action_buttons_component)
        return reports_table

    def switch_computer_fix(self, computer_fix: ComputerFixRequest2):
        if computer_fix is None:
            return
        send_switch_message_in_email(computer_fix)
        computer_fix.closed = not computer_fix.closed
        computer_fix.save()
        self.draw_tables()

    def delete_computer_fix(self, computer_fix: ComputerFixRequest2):
        if computer_fix is None:
            return
        send_delete_msg_in_email(computer_fix)
        computer_fix.delete()
        self.draw_tables()

    def edit_req_deadline(self, request):
        def save_request(x):
            request.finish_deadline = x.new_deadline
            request.save()
            self.draw_tables()

        class DeadlineEditForm(Document):
            new_deadline: datetime.datetime = DateField()

        form = JsonSchemaForm(
            DeadlineEditForm,
            value=DeadlineEditForm(new_deadline=request.finish_deadline),
            visible=['new_deadline'],
            display_name={'new_deadline': 'דדליין לסיום'},
            placeholder={},
            options={},
            options_display={},
            submit=save_request
        )

        self.popup = PopUp(form, title="עריכת דדליין", is_shown=True, is_cancelable=True)
        self.reports_stack.add_component(self.popup)

    def edit_req_in_tamam(self, request):
        def save_request(x):
            request.is_computer_in_tamam = x.is_computer_in_tamam
            request.save()
            self.draw_tables()

        class IsInTamamForm(Document):
            is_computer_in_tamam: str = StringField()

        form = JsonSchemaForm(
            IsInTamamForm,
            value=IsInTamamForm(is_computer_in_tamam=request.is_computer_in_tamam),
            visible=['is_computer_in_tamam'],
            display_name={'is_computer_in_tamam': 'האם המחשב הועבר לתממ?'},
            placeholder={},
            options={'is_computer_in_tamam': ['כן', 'לא']},
            options_display={'is_computer_in_tamam': lambda x: x},
            submit=save_request
        )

        self.popup = PopUp(form, title="עריכת סטטוס", is_shown=True, is_cancelable=True)
        self.reports_stack.add_component(self.popup)

    def edit_req_status(self, request, fix_request: ComputerFixRequest2):
        def save_request(x):
            request.statuses.append(x.new_status)
            request.save()
            send_status_in_email(request)
            self.draw_tables()

        class StatusEditForm(Document):
            new_status: str = StringField()

        form = JsonSchemaForm(
            StatusEditForm,
            visible=['new_status'],
            display_name={'new_status': 'סטטוס'},
            placeholder={'status': 'סטטוס תקלה'},
            options={},
            options_display={},
            paragraphTexts=['new_status'],
            submit=save_request
        )

        self.popup = PopUp(form, title="עריכת סטטוס", is_shown=True, is_cancelable=True)
        self.reports_stack.add_component(self.popup)

    def is_in_tamam_component(self, fix_request, is_computer_in_tamam):
        is_in_tamam_sp = StackPanel([])
        is_in_tamam_sp.add_component(Label(is_computer_in_tamam))
        is_in_tamam_sp.add_component(Button("ערוך", action=lambda req=fix_request: self.edit_req_in_tamam(req)))
        return is_in_tamam_sp

    def deadline_component(self, fix_request, finish_deadline):
        deadline_sp = StackPanel([])
        deadline_sp.add_component(Label(finish_deadline if finish_deadline is not None else "לא הוזן"))
        deadline_sp.add_component(Button("ערוך", action=lambda req=fix_request: self.edit_req_deadline(req)))
        return deadline_sp

    def statuses_component(self, fix_request, statuses):
        status_sp = StackPanel([])
        for j, status in enumerate(reversed(statuses)):
            status_sp.add_component(Label(status, size=SIZE_MEDIUM if j == 0 else SIZE_SMALL))
        if len(statuses) == 0:
            status_sp.add_component(Label("לא עודכן"))

        status_sp.add_component(
            Button("עדכן", action=lambda req=fix_request: self.edit_req_status(req, fix_request)))
        return status_sp

    def action_buttons_component(self, fix_request):
        button_sp = StackPanel([])
        if permissions.is_user_rasap(self.user):
            button_sp.add_component(
                Button("פתח מחדש" if fix_request.closed else "סגור תקלה",
                       action=lambda fix_request=fix_request: self.switch_computer_fix(fix_request))
            )
        if self.user == fix_request.user or permissions.is_user_rasap(self.user):
            button_sp.add_component(
                Button("מחק תקלה", action=lambda fix_request=fix_request: self.delete_computer_fix(fix_request),
                       bg_color='red')
            )
        return button_sp

    def create_request(self):
        def save_request(request: ComputerFixRequest2):
            request.statuses = []
            request.user = self.user
            request.time = datetime.datetime.now()
            request.closed = False
            request.save()
            self.draw_tables()
            self.popup.hide()
            send_request_in_email(request)

        form = JsonSchemaForm(ComputerFixRequest2,
                              visible=["computer_id", 'fix_type', 'is_computer_working',
                                       'description', 'is_computer_in_tamam', 'computer_serial'],
                              display_name={
                                  "computer_id": 'מזהה מחשב',
                                  'fix_type': 'סוג תקלה',
                                  'description': 'תיאור התקלה',
                                  'is_computer_in_tamam': 'האם המחשב הועבר לתממ?',
                                  'is_computer_working': 'האם המחשב שמיש כרגע?',
                                  'computer_serial': 'סיריאלי של מחשב',
                              },
                              placeholder={
                                  "computer_id": ' לדוגמה: TLP-D-109',
                                  'description': 'תיאור התקלה',
                              },
                              options={
                                  'fix_type': FixTypes.get_list(),
                                  'is_computer_in_tamam': ['כן', 'לא'],
                                  'is_computer_working': ['כן', 'לא']
                              },
                              options_display={
                                  'fix_type': lambda x: x,
                                  'is_computer_in_tamam': lambda x: x,
                                  'is_computer_working': lambda x: x,
                              },
                              submit=save_request)

        self.popup = PopUp(form, title="דיווח על תקלת מחשוב", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)
