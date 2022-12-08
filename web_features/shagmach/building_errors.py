import datetime
from mongoengine.document import Document
from mongoengine.fields import StringField
from mongoengine.queryset.visitor import Q

from web_features.shagmach.rasaput_utils import *
import web_features.shagmach.permissions as permissions
from web_framework.server_side.infastructure.constants import *
from APIs.TalpiotAPIs.Shagmach.building_fix_request import BuildingFixRequest
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanelColumn, \
    DocumentGridPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page


class BuildingErrors(Page):
    @staticmethod
    def get_title() -> str:
        return "תקלות בינוי"

    def report(self):
        pass

    def __init__(self, params):
        super().__init__()
        self.sp = StackPanel([])

        self.container_table = None
        self.popup = None
        self.open_reports_stack = StackPanel([])
        self.reported_stack = StackPanel([])
        self.closed_reports_stack = StackPanel([])

    def get_page_ui(self, user):
        self.user = user

        self.sp.add_component(Label("הצגת תקלות בינוי", size=SIZE_EXTRA_LARGE))
        self.sp.add_component(Button("דווח/י על תקלת בינוי", self.create_request))

        self.sp.add_component(
            Label(
                f"{len(BuildingFixRequest.objects((Q(closed=False) | Q(closed=None)) & (Q(is_reported=False) | Q(is_reported=None))))} תקלות פתוחות",
                size=SIZE_LARGE))
        self.sp.add_component(Divider())
        self.sp.add_component(self.open_reports_stack)

        self.sp.add_component(
            Label(
                f"{len(BuildingFixRequest.objects((Q(closed=False) | Q(closed=None)) & Q(is_reported=True)))} תקלות שדווחו",
                size=SIZE_LARGE))
        self.sp.add_component(Divider())
        self.sp.add_component(self.reported_stack)

        self.sp.add_component(Label(f"{len(BuildingFixRequest.objects(closed=True))} תקלות סגורות", size=SIZE_LARGE))
        self.sp.add_component(Divider())
        self.sp.add_component(self.closed_reports_stack)

        self.draw_tables()

        return self.sp

    def draw_tables(self):
        self.open_reports_stack.clear()
        self.open_reports_stack.add_component(self.get_reports_table(is_closed=False, is_reported=False))
        self.reported_stack.clear()
        self.reported_stack.add_component(self.get_reports_table(is_closed=False, is_reported=True))
        self.closed_reports_stack.clear()
        self.closed_reports_stack.add_component(self.get_reports_table(is_closed=True))

    def get_reports_table(self, is_closed, is_reported=True):
        reports_table = DocumentGridPanel(
            BuildingFixRequest,
            column_list=[
                DocumentGridPanelColumn('user', "שם",
                                        component_parser=lambda request, user: Label(f"{user.name} - {user.mahzor}")),
                DocumentGridPanelColumn('building', "מקום"),
                DocumentGridPanelColumn('floor', "קומה"),
                DocumentGridPanelColumn('room', "חדר"),

                DocumentGridPanelColumn('description', "תיאור התקלה"),
                DocumentGridPanelColumn('statuses', "סטטוס", self.statuses_component),
            ], filter_by={'closed': is_closed, "is_reported": is_reported}
        )
        reports_table.add_column(self.action_buttons_component)
        return reports_table

    def switch_building_fix(self, building_fix: BuildingFixRequest):
        if building_fix is None:
            return
        building_fix.closed = not building_fix.closed
        building_fix.save()
        self.draw_tables()

    def delete_building_fix(self, building_fix: BuildingFixRequest):
        if building_fix is None:
            return
        building_fix.delete()
        self.draw_tables()

    def edit_req_status(self, request, fix_request: BuildingFixRequest):
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
        self.open_reports_stack.add_component(self.popup)

    def statuses_component(self, fix_request, statuses):
        status_sp = StackPanel([])
        for j, status in enumerate(reversed(statuses)):
            status_sp.add_component(Label(status, size=SIZE_MEDIUM if j == 0 else SIZE_SMALL))
        if len(statuses) == 0:
            status_sp.add_component(Label("לא עודכן"))
        if permissions.is_user_rasap(self.user):
            status_sp.add_component(
                Button("עדכן", action=lambda req=fix_request: self.edit_req_status(req, fix_request)))
        return status_sp

    def action_buttons_component(self, fix_request):
        button_sp = StackPanel([])
        if permissions.is_user_rasap(self.user):
            if fix_request.is_reported:
                if not fix_request.closed:
                    button_sp.add_component(
                        Button("סגור תקלה",
                               action=lambda fix_request=fix_request: self.switch_building_fix(fix_request))
                    )
            else:
                button_sp.add_component(
                    Button("דווח",
                           action=lambda fix_request=fix_request: self.report_to_university(fix_request)))
        if self.user == fix_request.user or permissions.is_user_rasap(self.user):
            button_sp.add_component(
                Button("מחק תקלה", action=lambda fix_request=fix_request: self.delete_building_fix(fix_request),
                       bg_color='red')
            )
        return button_sp

    def report_to_university(self, building_fix: BuildingFixRequest):
        if building_fix is None:
            return
        building_fix.is_reported = True
        building_fix.save()
        self.draw_tables()

    def create_request(self):
        def save_request(request: BuildingFixRequest):
            request.statuses = []
            request.user = self.user
            request.time = datetime.datetime.now()
            request.closed = False
            request.is_reported = False
            request.save()
            self.draw_tables()
            self.popup.hide()

        form = JsonSchemaForm(BuildingFixRequest,
                              visible=["building", 'floor', 'room', 'description'],
                              display_name={
                                  "building": 'בניין',
                                  'floor': 'קומה',
                                  'room': 'חדר',
                                  'description': 'תיאור',
                              },
                              placeholder={
                                  'description': 'תיאור התקלה',
                              },
                              options={
                                  'building': ['מתל"מ', 'בית צרפת', "אודיטוריום"],
                              },
                              options_display={
                                  'building': lambda x: x,
                              },
                              submit=save_request)

        self.popup = PopUp(form, title="דיווח על תקלת בינוי", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)
