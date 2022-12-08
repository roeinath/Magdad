# from general import *
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.constants import *

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
from web_framework.server_side.infastructure.constants import *
from APIs.TalpiotAPIs.static_fields import get_static_fields, StaticFields, get_mahzor_number_list
from APIs.TalpiotAPIs.Group.division_group import DivisionGroup
from APIs.TalpiotAPIs.Group.group import Group


class GroupsEdit(Page):
    @staticmethod
    def get_title() -> str:
        return "עריכת קבוצות"

    @staticmethod
    def is_authorized(user: User):
        return MATLAM in user.role  # Only the people of the base

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

        my_groups = Group.objects(admins__contains=self.user)

        self.sp.add_component(Button("צור קבוצה", self.create_group))

        grid = GridPanel(len(my_groups), 3)
        self.sp.add_component(grid)

        i = 0
        for group in my_groups:
            grid.add_component(Label(group.name), i, 0)
            grid.add_component(Button("ערוך", lambda g=group: self.edit_group(g)), i, 1)
            grid.add_component(Button("מחק", lambda g=group: self.delete_group(g)), i, 2)
            i+=1

    def delete_group(self, group):
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
                'participants': User.objects(mahzor__in=get_mahzor_number_list()),
            }, 
            options_display= {
                'commander': lambda x: x.name + "-" + str(x.mahzor),
                'participants': lambda x: x.name + "-" + str(x.mahzor),
                'admins': lambda x: x.name + "-" + str(x.mahzor),
            }, 
            submit= save_group)

        self.popup = PopUp(form, title="יצירת קבוצה", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def edit_group(self, group):
        def save_group(x):
            group.name = x.name
            group.admins = x.admins
            group.participants = x.participants
            group.save()
            self.draw()

        form = JsonSchemaForm(Group, visible=['name', "admins", "participants"], 
            value=group,
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
                'participants': User.objects(mahzor__in=get_mahzor_number_list()),
            }, 
            options_display= {
                'commander': lambda x: x.name + "-" + str(x.mahzor),
                'participants': lambda x: x.name + "-" + str(x.mahzor),
                'admins': lambda x: x.name + "-" + str(x.mahzor),
            }, 
            submit= save_group)

        self.popup = PopUp(form, title="עריכת קבוצה", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)



