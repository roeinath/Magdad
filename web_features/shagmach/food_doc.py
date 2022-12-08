import os

import web_features.shagmach.permissions as permissions
from web_framework.server_side.infastructure.constants import *
from APIs.TalpiotAPIs.Food.food_request import FoodRequest
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanel
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanelColumn
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page

cur_dir = os.path.dirname(os.path.abspath(__file__))


class FoodDoc(Page):
    @staticmethod
    def get_title() -> str:
        return "עמוד מזון"

    def __init__(self, params):
        super().__init__()
        self.sp = StackPanel([])

        self.container_table = None
        self.popup = None
        self.orders_stack = StackPanel([])
        self.closed_orders_stack = StackPanel([])
        self.user = None

    def get_page_ui(self, user):
        self.user = user

        self.sp.add_component(Label("דוק בקשות מזון לאירועים"
                                    , size=SIZE_EXTRA_LARGE))
        with open(os.path.join(cur_dir, 'food_doc_explanation.txt'), 'r') as f:
            self.sp.add_component(Label(f.read(), size=SIZE_MEDIUM))

        self.sp.add_component(Button("הזמן מזון לאירוע", self.create_request))

        self.sp.add_component(Label("הזמנות קיימות", size=SIZE_LARGE))
        self.sp.add_component(Divider())
        self.sp.add_component(self.orders_stack)

        self.sp.add_component(Label("הזמנות שאושרו", size=SIZE_LARGE))
        self.sp.add_component(Divider())
        self.sp.add_component(self.closed_orders_stack)

        self.draw_tables()

        return self.sp

    def delete_order(self, order: FoodRequest):
        if order is None:
            return
        order.delete()
        self.draw_tables()

    def draw_action_buttons(self, fix_request):
        button_sp = StackPanel([])
        button_sp.add_component(
            Button("הבקשה לא טופלה" if fix_request.closed else "הבקשה טופלה",
                   action=lambda fix_request=fix_request: self.switch_order_closed(fix_request)))
        if fix_request.closed:
            button_sp.add_component(Button("מחק בקשה",
                       action=lambda fix_request=fix_request: self.delete_order(fix_request)))

        # if self.user == fix_request.user or permissions.is_user_rasap(self.user):
        #     button_sp.add_component(
        #         Button("מחיקת הבקשה", action=lambda fix_request=fix_request: self.delete_blay_fix(fix_request),
        #                bg_color='red')
        #     )
        return button_sp

    def switch_order_closed(self, order: FoodRequest):
        if order is None:
            return
        order.closed = not order.closed
        order.save()
        self.draw_tables()

    def create_request(self):
        def save_request(request: FoodRequest):
            request.statuses = []
            request.user = self.user
            request.closed = False
            request.is_reported = False
            request.save()
            self.draw_tables()
            self.popup.hide()
            # send_request_in_email(request)

        form = JsonSchemaForm(FoodRequest,
                              visible=['event', 'date', 'hour', 'description', 'FoodLimitations',
                                       'comments', 'RelevantAuthorities'],
                              display_name={
                                  "event": 'אירוע:',
                                  'date': 'תאריך:',
                                  'hour': 'שעת המשיכה:',
                                  'description': 'סוג הכיבוד:',
                                  'FoodLimitations': 'מענה לצמחונים/צליאקים/הגבלות מזון נוספות:',
                                  'execution': 'כיצד תתבצע המשיכה?',
                                  'equipment': 'ציוד נוסף שצריך למשיכה:',
                                  'comments': 'הערות נוספות:',
                                  'RelevantAuthorities': 'האם תואם מול הגורמים הרלוונטיים (קמטים/קמ"ד מנהלה)',

                              },
                              placeholder={
                                  'description': 'כיבוד א, כיבוד ב, אחר',
                                  'execution': 'כמה אנשים? האם צריך רכב?',
                                  'equipment': 'סכו"ם, קומקום, מיחם',
                                  'comments': 'כל דבר שצריף להוסיף מלאו פה',

                              },
                              submit=save_request)

        self.popup = PopUp(form, title="הזמנה חדשה", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def draw_tables(self):
        self.orders_stack.clear()
        self.orders_stack.add_component(self.get_orders_table(is_closed=False,
                                                              in_charge=permissions.is_user_food_allowed(self.user)))
        self.closed_orders_stack.clear()
        self.closed_orders_stack.add_component(self.get_orders_table(is_closed=True,
                                                                     in_charge=permissions.is_user_food_allowed(
                                                                         self.user)))

    def get_orders_table(self, is_closed, in_charge=False):
        orders_table = DocumentGridPanel(
            FoodRequest,
            column_list=[
                DocumentGridPanelColumn('user', "שם",
                                        component_parser=lambda request, user: Label(f"{user.name} - {user.mahzor}")),
                DocumentGridPanelColumn('event', "אירוע"),
                DocumentGridPanelColumn('date', "תאריך"),
                DocumentGridPanelColumn('hour', "שעת המשיכה"),
                DocumentGridPanelColumn('description', "סוג מזון"),
                DocumentGridPanelColumn('FoodLimitations', "הגבלות מזון"),
                DocumentGridPanelColumn('comments', "הערות"),
                DocumentGridPanelColumn('RelevantAuthorities', "תואם מול גורמים רלוונטיים")
            ], filter_by=({'closed': is_closed} if in_charge else {'user': self.user} and {'closed': is_closed})
        )

        if permissions.is_user_food_allowed(self.user):
            orders_table.add_column(self.draw_action_buttons)

        return orders_table
