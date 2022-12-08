from mongoengine import *

import web_features.shagmach.permissions as permissions
from web_framework.server_side.infastructure.constants import *
from APIs.TalpiotAPIs.Shagmach.blay_request import ItemFixRequest, ItemTypes
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanelColumn
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page


class BlayRequests(Page):
    @staticmethod
    def get_title() -> str:
        return "בקשות בלאי"

    def __init__(self, params):
        super().__init__()
        self.sp = StackPanel([])

        self.container_table = None
        self.popup = None
        self.reports_stack = StackPanel([])
        self.closed_reports_stack = StackPanel([])
        self.user = None

    def get_page_ui(self, user):
        self.user = user

        self.sp.add_component(Label("הצגת בקשות בלאי", size=SIZE_EXTRA_LARGE))
        self.sp.add_component(Button("דווח/י על בלאי", self.create_request))

        self.sp.add_component(Label("בלאי שהוגש", size=SIZE_LARGE))
        self.sp.add_component(Divider())
        self.sp.add_component(self.reports_stack)

        self.sp.add_component(Label("בקשות סגורות", size=SIZE_LARGE))
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
            ItemFixRequest,
            column_list=[
                DocumentGridPanelColumn('user', "שם",
                                        component_parser=lambda request, user: Label(user.get_full_name())),
                DocumentGridPanelColumn('soldier_id', "מספר אישי",
                                        component_parser=lambda request, soldier_id: Label(soldier_id or 'חסר')),
                DocumentGridPanelColumn('item_type', "סוג פריט"),
                DocumentGridPanelColumn('amount', "כמות"),
                DocumentGridPanelColumn('reason', "סיבה"),
                DocumentGridPanelColumn('size_required', "מידה"),
                DocumentGridPanelColumn('comment', "הערות", component_parser=self.draw_comment_column)
            ], filter_by={'closed': is_closed}
        )
        reports_table.add_column(self.draw_action_buttons)
        return reports_table

    def draw_action_buttons(self, fix_request):
        button_sp = StackPanel([])
        if permissions.is_user_rasap(self.user):
            button_sp.add_component(
                Button("הגשה מחדש" if fix_request.closed else "סגירת הבקשה",
                       action=lambda fix_request=fix_request: self.switch_blay_fix(fix_request))
            )
        if self.user == fix_request.user or permissions.is_user_rasap(self.user):
            button_sp.add_component(
                Button("מחיקת הבקשה", action=lambda fix_request=fix_request: self.delete_blay_fix(fix_request),
                       bg_color='red')
            )
        return button_sp

    def switch_blay_fix(self, blay_fix: ItemFixRequest):
        if blay_fix is None:
            return
        blay_fix.closed = not blay_fix.closed
        blay_fix.save()
        self.draw_tables()

    def delete_blay_fix(self, blay_fix: ItemFixRequest):
        if blay_fix is None:
            return
        blay_fix.delete()
        self.draw_tables()

    def draw_comment_column(self, request, comment):
        comment_sp = StackPanel([])
        comment_sp.add_component(Label(comment if comment is not None else ""))
        if self.user == request.user or permissions.is_user_rasap(self.user):
            comment_sp.add_component(Button("ערוך", action=lambda req=request: self.edit_req_comment(req)))
        return comment_sp

    def edit_req_comment(self, request):
        def save_request(x):
            request.comment = x.comment
            request.save()
            self.draw_tables()

        class CommentEditForm(Document):
            comment: str = StringField()

        form = JsonSchemaForm(
            CommentEditForm,
            value=CommentEditForm(comment=request.comment),
            visible=['comment'],
            display_name={'comment': 'הערה'},
            placeholder={},
            options={},
            options_display={},
            submit=save_request
        )

        self.popup = PopUp(form, title="עריכת הערות", is_shown=True, is_cancelable=True)
        self.reports_stack.add_component(self.popup)

    def create_request(self):
        def save_request(request):
            request.closed = False
            request.user = self.user
            request.save()
            self.draw_tables()
            self.popup.hide()

        form = JsonSchemaForm(
            ItemFixRequest,
            visible=['soldier_id', 'item_type', 'amount', 'reason', 'size_required'],
            display_name={
                'soldier_id': 'מספר אישי',
                'item_type': 'סוג פריט',
                'amount': 'כמות',
                'reason': 'סיבה',
                'size_required': 'מידה מבוקשת'
            },
            placeholder={
                'amount': 'כמות',
                'reason': 'לדוגמא: בלאי, מידה לא מתאימה'
            },
            options={
                'item_type': ItemTypes.get_list(),
                'size_required': ['אחר', 'לא רלוונטי', '48', '47', '46', '45', '44', '43', '42', '41', '40', '39',
                                  '38', '37', '36', '35', 'ממ', 'מ', 'ג', 'ב', 'ק'],
            },
            submit=save_request
        )

        self.popup = PopUp(form, title="דיווח על בלאי", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)
