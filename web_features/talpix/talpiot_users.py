# from general import *
from mongoengine import Document, ListField, StringField, ReferenceField

from APIs.TalpiotAPIs import User, SecretCodeManager
from web_features.talpix import permissions
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.confirmation_button import ConfirmationButton
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanel, \
    DocumentGridPanelColumn
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page


class TalpiotUsers(Page):
    def __init__(self, params):
        super().__init__()

        self.sp = None
        self.grid = None
        self.popup = None

    def mark_interested(self, request):
        pass

    @staticmethod
    def get_title() -> str:
        return "משתמשים"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_developer(user)

    class GuardingSettingsForm(Document):
        not_guarding = ListField(ReferenceField(User))
        calendar_id = StringField()

    def save_user(self, user, obj):
        user.email = obj.email
        user.name = obj.name
        user.mahzor = obj.mahzor
        user.gender = obj.gender
        user.team_commander = obj.team_commander
        user.mahzor_commander = obj.mahzor_commander
        user.phone_number = obj.phone_number
        user.telegram_id = obj.telegram_id
        user.mahzor_admin = obj.mahzor_admin
        user.bot_admin = obj.bot_admin
        user.birthday = obj.birthday
        user.role = obj.role
        user.secret_code = obj.secret_code if obj.secret_code else SecretCodeManager.generate_code()

        user.save()

        self.show_information()

    def edit_user(self, user):
        users = list(User.objects)

        get_user_name = lambda x: x.name

        form = JsonSchemaForm(
            User,
            value=user,
            visible=['email',
                     'name',
                     'mahzor',
                     'gender',
                     'team_commander',
                     'mahzor_commander',
                     'phone_number',
                     'telegram_id',
                     'mahzor_admin',
                     'bot_admin',
                     # 'birthday',
                     'role', 'secret_code'],
            display_name={
                'email': 'מייל',
                'name': 'שם',
                'mahzor': 'מחזור',
                'gender': 'מין',
                'team_commander': 'מפקצ',
                'mahzor_commander': 'מפקד/ת מחזור',
                'phone_number': 'טלפון',
                'telegram_id': 'טלגרם ID',
                'mahzor_admin': 'האם חנתר',
                'bot_admin': 'צוות בוט',
                'birthday': 'יום הולדת',
                'role': 'תפקידים',
                'secret_code': 'קוד סודי',
            },
            options={
                'team_commander': users,
                'mahzor_commander': users,
            }, options_display={
                'team_commander': get_user_name,
                'mahzor_commander': get_user_name
            }, submit=lambda x, u=user: self.user.bot_admin and self.save_user(user, x)
        )
        self.popup = PopUp(form, title="עריכת משתמש", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def add_user(self):
        if not self.user.bot_admin:
            return

        form = JsonSchemaForm(User,
                              visible=['email',
                                       'name',
                                       'mahzor',
                                       'gender',
                                       'phone_number'],
                              display_name={
                                  'email': 'מייל',
                                  'name': 'שם',
                                  'mahzor': 'מחזור',
                                  'gender': 'מין',
                                  'phone_number': 'טלפון'
                              },
                              options={"gender": ["male", "female"]},
                              submit=lambda x: self.save_user(x, x))

        # self.sp.add_component(form)

        self.popup = PopUp(form, title="הוספת משתמש", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    class FilterForm(Document):
        order_by = ListField(StringField())
        filter_by = ListField(StringField())

    def show_filters(self):
        # form = JsonSchemaForm(TalpiotUsers.FilterForm, value=self.filters,
        #   visible=['order_by', 'filter_by'],
        #   display_name={
        #         'order_by': "מיין",
        #         'filter_by': "סנן"
        #     }, options={
        #         'order_by': [
        #             {"id": "mahzor", "title": "מחזור"},
        #             {"id": "name", "title": "שם"},
        #         ],
        #         'filter_by': [
        #             {"id": "mahzor", "title": "מחזור"},
        #             {"id": "name", "title": "שם"},
        #         ],
        #     }, options_display={
        #         'team_commander': user_name,
        #         'mahzor_commander': user_name
        #     }, submit= lambda x, u=user: self.save_user(user, x))
        #
        # #self.sp.add_component(form)
        #
        # self.popup = PopUp(form, title="עריכת משתמש", is_shown=True, is_cancelable=True)
        # self.sp.add_component(self.popup)

        pass

    def show_information(self):
        self.sp.clear()

        users = User.objects.order_by('-mahzor')

        titles = {
            "name": "שם",
            "mahzor": "מחזור"
        }

        self.grid = GridPanel(len(users) + 1, len(titles.keys()) + 1, bg_color='talpiot_cyan')
        self.sp.add_component(Label("משתמשים", size=SIZE_EXTRA_LARGE))
        self.sp.add_component(Button("הוסף", lambda: self.add_user()))
        self.sp.add_component(self.grid)

        users_mahzors = sorted({u.mahzor for u in User.objects()}, reverse=True)
        users_tables = []
        for mahzor_num in users_mahzors:
            table_for_mahzor = DocumentGridPanel(User, [
                DocumentGridPanelColumn("mahzor", "מחזור"),
                DocumentGridPanelColumn("name", "שם")
            ], filter_by={'mahzor': mahzor_num}, order_by=['name'])
            table_for_mahzor.add_column(lambda user: Button("ערוך", lambda u=user: self.edit_user(u)))
            users_tables.append(table_for_mahzor)

        self.sp.add_component(Accordion(users_tables, [str(i) for i in users_mahzors]))

    def get_page_ui(self, user):
        self.user = user
        self.sp = StackPanel([])

        self.show_information()

        return self.sp
