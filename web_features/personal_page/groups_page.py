from APIs.TalpiotAPIs.Group import CommandedGroup

from web_framework.server_side.infastructure.page import Page
# standard Talpix page class to inherit from.
from APIs.TalpiotAPIs import User
from web_framework.server_side.infastructure.constants import *
from typing import Tuple, Dict, List
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.getdata.academy_grades_interface import *
from web_features.personal_page.modules.groups_classes import GroupsGrades, GroupSkira, CompareStats
from web_features.personal_page.modules.constants import *
from web_features.personal_page.permissions import *

MAHZOR_DICT = {"43": "מג", "42": "מב", "41": "מא"}


class GroupsPage(Page):
    """
    This page contains data of groups - academia and program's indexes.
    """

    def __init__(self, params):
        super().__init__(params)
        self.selected_sem = None
        self.user = None
        self.gp = GridPanel(3, 1, bordered=False)
        self.mahzor_groups = {}
        self.mahzor_years = {}
        self.selected_year = None
        self.selected_mahzor = None
        self.selected_group = None

    @staticmethod
    def get_title():
        return "נתוני קבוצות"

    @staticmethod
    def is_authorized(user):
        return is_user_X_admin(user) or is_user_captain(user) or is_group_data_authorized(user)

    # TODO: update the page_ui with deafault
    # def get_page_ui(self, user: User):
    #     self.user = user
    #
    #     self.options_layout = GridPanel(2, 4, bg_color=COLOR_PRIMARY_DARK)
    #
    #     # Labels
    #     self.options_layout.add_component(Label("מחזור", fg_color='White'), 0, 3)
    #     self.options_layout.add_component(Label("קבוצה", fg_color='White'), 0, 2)
    #     self.options_layout.add_component(Label("שנה", fg_color='White'), 0, 1)
    #     self.options_layout.add_component(Label("סמסטר", fg_color='White'), 0, 0)
    #     # Options
    #
    #     if is_user_captain(user):
    #         self.mahzor_combo = ComboBox(mahzor_numstr_to_letters,
    #                                      on_changed=lambda selected_mahzor: self.load_groups(selected_mahzor),
    #                                      default_value=str(
    #                                          CommandedGroup.objects(commander=user).select_related(1)[0].participants[
    #                                              0].mazhor))
    #     else:
    #         self.mahzor_combo = ComboBox(mahzor_numstr_to_letters,
    #                                      on_changed=lambda selected_mahzor: self.load_groups(selected_mahzor),
    #                                      default_value=str(self.user.mahzor))
    #
    #     self.options_layout.add_component(self.mahzor_combo, 1, 3)
    #
    #     # need to be changed
    #
    #     if is_user_captain(user):
    #         self.mahzor_groups = CommandedGroup.objects(commander=user)
    #         self.selected_mahzor = CommandedGroup.objects(commander=user).select_related(1)[0].participants[0].mazhor
    #     else:
    #         self.load_groups(str(self.user.mahzor))
    #         self.selected_mahzor = self.user.mahzor
    #     print(self.mahzor_groups)
    #     self.group_combo_box = ComboBox(self.mahzor_groups, on_changed=lambda group: self.change_group(group),
    #                                     default_value=Group.objects(group_tags=[str(
    #                                         self.selected_mahzor)]).select_related(1)[0].name)
    #
    #     self.change_group(Group.objects(group_tags=[str(
    #         self.selected_mahzor)]).select_related(1)[0].name)
    #
    #     self.options_layout.add_component(self.group_combo_box, 1, 2)
    #
    #     self.year_combo_box = ComboBox(self.mahzor_years,
    #                                    on_changed=lambda year: self.change_year(year),
    #                                    default_value=self.mahzor_years["2022"])
    #     self.change_year(self.mahzor_years["2022"])
    #     self.options_layout.add_component(self.year_combo_box, 1, 1)
    #
    #     self.sem_combo_box = ComboBox({"A": "א", "B": "ב"},
    #                                   on_changed=lambda year: self.change_sem(year),
    #                                   default_value=str("A"))
    #     self.change_sem(str("A"))
    #     self.options_layout.add_component(self.sem_combo_box, 1, 0)
    #
    #     self.gp.add_component(self.options_layout, 0, 0)
    #     self.gp.add_component(Button("טען ציונים", self.load_grades), 1, 0)
    #     self.load_grades()
    #     return self.gp

    def get_page_ui(self, user: User):
        self.user = user

        self.options_layout = GridPanel(2, 4, bg_color=COLOR_PRIMARY_DARK)

        # Labels
        self.options_layout.add_component(Label("מחזור", fg_color='White'), 0, 3)
        self.options_layout.add_component(Label("קבוצה", fg_color='White'), 0, 2)
        self.options_layout.add_component(Label("שנה", fg_color='White'), 0, 1)
        self.options_layout.add_component(Label("סמסטר", fg_color='White'), 0, 0)
        # Options

        if is_user_captain(user):
            self.selected_mahzor = 43
        else:
            self.selected_mahzor = self.user.mahzor
        self.mahzor_combo = ComboBox(mahzor_numstr_to_letters,
                                     on_changed=lambda selected_mahzor: self.load_groups(selected_mahzor),
                                     default_value=str(self.selected_mahzor))

        self.options_layout.add_component(self.mahzor_combo, 1, 3)

        self.load_groups(str(self.selected_mahzor))

        print(self.mahzor_groups)
        self.group_combo_box = ComboBox(self.mahzor_groups, on_changed=lambda group: self.change_group(group),
                                        default_value=Group.objects(group_tags=[str(
                                            self.selected_mahzor)]).select_related(1)[0].name)

        self.change_group(Group.objects(group_tags=[str(
            self.selected_mahzor)]).select_related(1)[0].name)

        self.options_layout.add_component(self.group_combo_box, 1, 2)

        self.year_combo_box = ComboBox(self.mahzor_years,
                                       on_changed=lambda year: self.change_year(year),
                                       default_value=self.mahzor_years["2022"])
        self.change_year(self.mahzor_years["2022"])
        self.options_layout.add_component(self.year_combo_box, 1, 1)

        self.sem_combo_box = ComboBox({"A": "א", "B": "ב"},
                                      on_changed=lambda year: self.change_sem(year),
                                      default_value=str("A"))
        self.change_sem(str("A"))
        self.options_layout.add_component(self.sem_combo_box, 1, 0)

        self.gp.add_component(self.options_layout, 0, 0)
        self.gp.add_component(Button("טען ציונים", self.load_grades), 1, 0)
        self.load_grades()
        return self.gp

    def load_grades(self):
        self.data_gp = GridPanel(2, 2)

        self.data_gp.add_component(Label("אקדמיה", size=SIZE_LARGE, bold=True), 0, 0)
        self.data_gp.add_component(Label("פלטפורמות", size=SIZE_LARGE, bold=True), 0, 1)
        self.data_gp.add_component(GroupsGrades(self.selected_group, self.selected_year, self.user).get_component(), 1,
                                   0)
        self.data_gp.add_component(GroupSkira(self.user, get_by_name_group(self.selected_group),
                                              self.selected_year, self.selected_year,
                                              self.selected_sem).get_component(),
                                   1, 1)

        self.gp.add_component(self.data_gp, 2, 0)

    def load_groups(self, mahzor):
        self.selected_mahzor = int(mahzor)
        self.mahzor_years = {str(year): str(year) for year in mahzor_number_to_years[self.selected_mahzor]}

        self.mahzor_groups = {}
        for group in Group.objects(group_tags=[str(self.selected_mahzor)]):
            group_name = group.name
            self.mahzor_groups[group_name] = group_name

        self.group_combo_box = ComboBox(self.mahzor_groups, on_changed=lambda group: self.change_group(group))
        self.options_layout.add_component(self.group_combo_box, 1, 2)

        self.year_combo_box = ComboBox(self.mahzor_years,
                                       on_changed=lambda year: self.change_year(year))
        self.options_layout.add_component(self.year_combo_box, 1, 1)

    def change_group(self, group):
        self.selected_group = group

    def change_year(self, year):
        self.selected_year = year

    def change_sem(self, sem):
        self.selected_sem = sem
