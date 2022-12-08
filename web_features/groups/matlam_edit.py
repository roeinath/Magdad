# from general import *
from mongoengine import *
from mongoengine.document import Document
from mongoengine.fields import IntField, ReferenceField, StringField

from APIs.TalpiotAPIs import SecretCodeManager
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.Group.division_group import DivisionGroup
from APIs.TalpiotAPIs.Group.mahzor_group import MahzorGroup
from APIs.TalpiotAPIs.Group.team_group import TeamGroup
from APIs.TalpiotAPIs.static_fields import get_static_fields, StaticFields, get_mahzor_number_list
from web_features.groups.add_users_from_csv import add_users_from_csv
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.upload_files import UploadFiles
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel, VERTICAL, HORIZONTAL
from web_framework.server_side.infastructure.page import Page


class MatlamEdit(Page):
    @staticmethod
    def get_title() -> str:
        return "עריכת מתלם"

    @staticmethod
    def is_authorized(user: User):
        return user.bot_admin

    def __init__(self, params):
        super().__init__()
        self.sp: StackPanel = StackPanel()
        self.static_fields: StaticFields = get_static_fields()
        self.user = None

    def draw(self):
        self.sp.clear()

        self.sp.add_component(Button("יצירת מחזור חדש", self.add_new_mahzor_popup))
        self.sp.add_component(Button("יצירת מחזור מחניכים לפי CSV", self.create_mahzor_from_csv))
        self.sp.add_component(Button("הוסף מחזור למתלם הנוכחי", self.add_mahzor_to_matlam_popup))

        mahzors_grid = GridPanel(20, 3)
        row = 0
        for mahzor in self.static_fields.current_mahzors:
            mahzor_block = StackPanel(orientation=HORIZONTAL)
            mahzor_block.add_component(Label(mahzor.name))
            mahzors_grid.add_component(mahzor_block, row, 0)

            for division in DivisionGroup.objects(mahzor=mahzor):
                division_block = StackPanel(orientation=HORIZONTAL)
                division_block.add_component(Label(division.name))
                division_block.add_component(Button(text="עריכה", action=lambda d=division: self.edit_division(d)))
                division_block.add_component(Button(text="מחיקה", action=lambda d=division: self.remove_item(d)))
                division_block.add_component(Button("הוסף צוות", lambda d=division: self.create_team_popup(d)))
                mahzors_grid.add_component(division_block, row, 1)
                division_teams = StackPanel(orientation=VERTICAL)

                for team in TeamGroup.objects(division=division):
                    team_block = StackPanel(orientation=HORIZONTAL)
                    team_block.add_component(Label(team.name))
                    team_block.add_component(Button(text="עריכה", action=lambda t=team: self.edit_team(t)))
                    team_block.add_component(Button(text="מחיקה", action=lambda t=team: self.remove_item(t)))
                    division_teams.add_component(team_block, row)

                mahzors_grid.add_component(division_teams, row, 2)
                row += 1

            mahzors_grid.add_component(Button("הסר מהמתלם הנוכחי", action=lambda m=mahzor: self.remove_item(m,
                                                                                                            self.remove_mahzor_from_matlam)),
                                       row, 2)
            mahzors_grid.add_component(Button("הוסף מחלקה", lambda m=mahzor: self.create_division_popup(m)), row, 1)
            row += 1

        self.sp.add_component(mahzors_grid)

    def get_page_ui(self, user):
        self.user = user
        self.draw()
        return self.sp

    def add_new_mahzor_popup(self):

        def create_mahzor(x):
            x.admins = [x.commander]
            x.save()

        form = JsonSchemaForm(MahzorGroup, visible=['name', 'mahzor_num', "commander", "participants"],
                              display_name={'name': 'שם', 'mahzor_num': 'מספר', "commander": 'מפקד/ת',
                                            'participants': 'חברי מחזור', },
                              options={'commander': User.objects,
                                       'participants': User.objects},
                              options_display={'commander': lambda x: x.get_full_name(),
                                               'participants': lambda x: x.get_full_name()},
                              submit=create_mahzor)

        self.popup = PopUp(form, title="יצירת מחזור", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def create_mahzor_from_csv(self):
        participants = []

        class MahzorFromNumberForm(Document):
            name: str = StringField()
            mahzor_num: int = IntField()
            commander: User = ReferenceField(User)

        def create_mahzor(x: MahzorFromNumberForm):
            if not participants:
                print("Error, CSV not valid")
                return
            for user in participants:
                if user.mahzor:
                    print(f"User {user.get_full_name()} already in mahzor {user.mahzor}")
                    continue
                user.mahzor = x.mahzor_num
                if not user.secret_code:
                    user.secret_code = SecretCodeManager.generate_code()
                user.save()
            mahzor = MahzorGroup(name=x.name, short_name=x.name, mahzor_num=x.mahzor_num, commander=x.commander,
                                 admins=[x.commander], participants=participants, group_tags=[str(x.mahzor_num)])
            mahzor.save()
            print("Created", mahzor.name, "with participants:", mahzor.participants)
            self.draw()

        form = JsonSchemaForm(
            MahzorFromNumberForm,
            visible=['name', 'mahzor_num', "commander"],
            display_name={'name': 'שם', 'mahzor_num': 'מספר', "commander": 'מפקד/ת'},
            options={'commander': User.objects, },
            options_display={'commander': lambda x: x.get_full_name()},
            submit=create_mahzor
        )
        upload_file = UploadFiles(upload_action=lambda files: add_users_from_csv(files[0], participants))
        self.popup = PopUp(upload_file, title="יצירת מחזור", is_shown=True, is_cancelable=True)
        self.popup.add_component(form)
        self.sp.add_component(self.popup)

    def add_mahzor_to_matlam_popup(self):
        class MahzorSelection(Document):
            mahzor = ReferenceField(MahzorGroup)

        def add_mahzor(x):
            self.static_fields.current_mahzors.append(x.mahzor)
            self.static_fields.save()
            self.draw()

        form = JsonSchemaForm(
            MahzorSelection,
            visible=['mahzor'],
            display_name={'mahzor': 'מחזור', },
            options={'mahzor': [g for g in MahzorGroup.objects if g not in self.static_fields.current_mahzors], },
            options_display={'mahzor': lambda x: x.name + "(" + str(x.mahzor_num) + ")", },
            submit=add_mahzor
        )

        self.popup = PopUp(form, title="הוספת מחזור", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def create_division_popup(self, mahzor):
        def create_division(x):
            x.admins = [x.commander]
            x.mahzor = mahzor
            x.save()
            self.draw()

        form = JsonSchemaForm(
            DivisionGroup,
            visible=['name', "commander", "participants"],
            display_name={'name': 'שם', "commander": 'מפקד/ת', 'participants': 'חברי מחלקה'},
            options={'commander': User.objects, 'participants': User.objects(mahzor=mahzor.mahzor_num)},
            options_display={'commander': lambda x: x.get_full_name(), 'participants': lambda x: x.get_full_name()},
            submit=create_division
        )

        self.popup = PopUp(form, title="יצירת מחלקה", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def create_team_popup(self, division):
        def create_team(x):
            x.admins = [x.commander]
            x.division = division
            x.save()
            self.draw()

        form = JsonSchemaForm(
            TeamGroup,
            visible=['name', "commander", "participants"],
            display_name={'name': 'שם', "commander": 'מפקד/ת', 'participants': 'חברי צוות', },
            options={'commander': User.objects, 'participants': division.participants},
            options_display={'commander': lambda x: x.get_full_name(),
                             'participants': lambda x: x.get_full_name()},
            submit=create_team
        )

        self.popup = PopUp(form, title="יצירת צוות", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def remove_item(self, item, delete_function=lambda d: d.delete()):
        def final_remove(i):
            delete_function(i)
            self.draw()

        self.popup = PopUp(Button("מחיקה", action=lambda i=item: final_remove(i)),
                           title="האם לבצע מחיקה?", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def remove_mahzor_from_matlam(self, mahzor):
        self.static_fields.current_mahzors.remove(mahzor)
        self.static_fields.save()
        self.draw()

    def edit_division(self, division):
        def save_division(x):
            division.name = x.name
            division.mahzor = x.mahzor
            division.commander = x.commander
            division.participants = x.participants
            division.save()
            self.draw()

        form = JsonSchemaForm(
            DivisionGroup,
            visible=['name', "mahzor", "commander", "participants"],
            value=division,
            display_name={'name': 'שם', 'mahzor': 'מחזור', "commander": 'מפקד/ת', 'participants': 'חברי מחלקה'},
            placeholder={},
            options={'mahzor': MahzorGroup.objects, 'commander': User.objects,
                     'participants': User.objects(mahzor=division.mahzor.mahzor_num)},
            options_display={'mahzor': lambda x: str(x.mahzor_num), 'commander': lambda x: x.get_full_name(),
                             'participants': lambda x: x.get_full_name()},
            submit=save_division
        )

        self.popup = PopUp(form, title="עריכת מחלקה", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def edit_team(self, team):
        def save_team(x):
            team.name = x.name
            team.division = x.division
            team.commander = x.commander
            team.participants = x.participants
            team.save()
            self.draw()

        form = JsonSchemaForm(
            TeamGroup,
            visible=['name', "division", "commander", "participants"],
            value=team,
            display_name={'name': 'שם', "commander": 'מפקד/ת', 'participants': 'חברי צוות',
                          'division': 'מחלקה', },
            options={'commander': User.objects, 'participants': team.division.participants,
                     'division': DivisionGroup.objects, },
            options_display={'commander': lambda x: x.get_full_name(),
                             'participants': lambda x: x.get_full_name(),
                             'division': lambda x: x.name},
            submit=save_team
        )

        self.popup = PopUp(form, title="עריכת צוות", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)
