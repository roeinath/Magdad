# from general import *
from mongoengine import *

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.Group import MahzorGroup, TeamGroup, DivisionGroup
from APIs.TalpiotAPIs.Group.group import Group
from APIs.TalpiotAPIs.static_fields import get_mahzor_number_list
from web_features.groups.permissions import is_user_admin
from web_framework.server_side.infastructure.actions import simple_send_message
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
from web_framework.server_side.infastructure.page import Page


class GroupsAdmins(Page):
    @staticmethod
    def get_title() -> str:
        return "עריכת קבוצות (אדמינים)"

    @staticmethod
    def is_authorized(user: User):
        return is_user_admin(user)

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

        self.sp.add_component(Label("עריכת קבוצות"))

        self.sp.add_component(Button("צור קבוצה", self.create_group))

        accordion = Accordion([self.get_group_table(MahzorGroup), self.get_group_table(DivisionGroup),
                                self.get_group_table(TeamGroup), self.get_group_table(Group)],
                  ["MahzorGroup", "DivisionGroup", "TeamGroup", "All"])
        self.sp.add_component(accordion)

    def get_group_table(self, group_class):
        return DocumentGridPanel(group_class, [
            DocumentGridPanelColumn("name", "שם"),
            DocumentGridPanelColumn("name", " ", lambda group, _: Button("ערוך", lambda g=group: self.edit_group(g))),
            DocumentGridPanelColumn("name", " ", lambda group, _: ConfirmationButton("מחק", lambda g=group:
                                                                                            self.delete_group(g))),
         ])

    def delete_group(self, group):
        if self.user.bot_admin:
            group.delete()
        self.draw()

    def create_group(self):
        def save_group(x):
            x.save()
            self.draw()

        form = JsonSchemaForm(Group, visible=['name', "admins", "participants"],
                              display_name={
                                  'name': 'שם',
                                  "admins": 'מנהלים',
                                  'participants': 'חברי קבוצה',
                              },
                              placeholder={
                              },
                              options={
                                  'commander': User.objects,
                                  'admins': User.objects,
                                  'participants': User.objects,
                              },
                              options_display={
                                  'commander': lambda x: x.name + "-" + str(x.mahzor),
                                  'participants': lambda x: x.name + "-" + str(x.mahzor),
                                  'admins': lambda x: x.name + "-" + str(x.mahzor),
                              },
                              submit=save_group)

        self.popup = PopUp(form, title="יצירת קבוצה", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def edit_group(self, group):
        def save_group(x):
            group.name = x.name
            group.admins = x.admins
            group.participants = x.participants
            group.group_tags = x.group_tags
            group.save()
            self.draw()
            simple_send_message(f"""הקבוצה {group.name} השתנתה:\n
            admins = {x.admins}
            participants = {x.participants}
            group_tags = {x.group_tags}""", user_list=list(User.objects(bot_admin=True)))

        form = JsonSchemaForm(Group, visible=['name', "admins", "participants", "group_tags"],
                              value=group,
                              display_name={
                                  'name': 'שם',
                                  "admins": 'מנהלים',
                                  'participants': 'חברי קבוצה',
                                  'group_tags': "מחזורים"
                              },
                              placeholder={
                              },
                              options={
                                  'commander': User.objects,
                                  'admins': User.objects,
                                  'participants': User.objects(mahzor__in=get_mahzor_number_list()),
                                  'group_tags': [str(x) for x in get_mahzor_number_list()]

                              },
                              options_display={
                                  'commander': lambda x: x.name + "-" + str(x.mahzor),
                                  'participants': lambda x: x.name + "-" + str(x.mahzor),
                                  'admins': lambda x: x.name + "-" + str(x.mahzor),
                                  'group_tags': lambda x: x
                              },
                              submit=save_group)

        self.popup = PopUp(form, title="עריכת קבוצה", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)
