from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_features.personal_page.permissions import *
from web_features.personal_page.modules.constants import *
from typing import Dict
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.getdata.skirot_grades_interface import *
from web_framework.server_side.infastructure.components.chartjs_component import ChartjsComponent
import time


# time generator for testing
def time_passed_generator():
    while True:
        yield time.time()


time_passed = time_passed_generator()
TEST = True
# description = ["דמות (מנהיגות)", "תפקוד בחברה (מנהיגות)", "הובלה (מנהיגות)",
#                "ניהול (מקצועיות)", "מדעי אקדמי (מקצועיות)", "מדעי יישומי (מקצועיות)", "בטחוני (מקצועיות)",
#                "א (ערכים)", "ד (ערכים)", "ה (ערכים)", "י (ערכים)", "מ (ערכים)"]

# Constant of page

NAME_OF_PAGE = "אזור הערכתי - קבוצות"

class CommanderGroupsPage(Page):
    def __init__(self, params):
        super().__init__(params)
        self.sp = None
        self.mahzor_names = {}
        self.title = ""
        self.options_table = None
        self.options_headers = None
        self.layout_table = None

    @staticmethod
    def get_title():
        return NAME_OF_PAGE

    @staticmethod
    def is_authorized(user):
        return is_user_captain(user) or is_user_X_admin(user)

    def avg_platforms_grade(self, counter_dict: Dict):

        self.avg_platforms_grades_of_group = {}
        for pg_enc in self.platform_grades:
            if counter_dict[pg_enc.platform] >= 3:
                pg_dec = pg_enc.decrypted_grades(is_real_data=is_user_captain(self.user))
                if pg_enc.platform not in self.avg_platforms_grades_of_group.keys():
                    self.avg_platforms_grades_of_group[pg_enc.platform] = {}
                    for key in pg_enc.grades.keys():
                        self.avg_platforms_grades_of_group[pg_enc.platform][key] = 0
                for key in pg_enc.grades.keys():
                    self.avg_platforms_grades_of_group[pg_enc.platform][key] += pg_dec[key]
        # print(self.avg_platforms_grades_of_group)
        for platform in self.avg_platforms_grades_of_group.keys():
            for key in self.avg_platforms_grades_of_group[platform].keys():
                self.avg_platforms_grades_of_group[platform][key] /= counter_dict[platform]

    def draw_graph_1(self, plat_grade: PlatformGrade):
        graph_label = "ציון - {0}".format(plat_grade.user.name)
        graph_1 = ChartjsComponent(width="35vw", height="35vw")

        graph_1.labels('r', size=15)
        avg_grades_platform = self.avg_platforms_grades_of_group[plat_grade.platform]
        description = [PARAM_DICT[a] for a in avg_grades_platform.keys()]  # list(filter(lambda key:
        # avg_grades_platform[key] >= 1,
        # avg_grades_platform.keys()))
        avg_grade = [val if val >= 1 else 0 for val in
                     avg_grades_platform.values()]  # list(filter(lambda val: val >= 1,avg_grades_platform.values()))
        graph_1.radar(description, avg_grade, label="ממוצע",
                      border_color=bg_color_dict[1])

        grades = plat_grade.decrypted_grades(is_real_data=is_user_captain(self.user))
        single_grade = grades.values()  # list(filter(lambda val: val >= 1, grades.values()))
        graph_1.scale('r', min=0, max=max(6, max(avg_grade), max(single_grade)))
        graph_1.radar(description, single_grade, label=graph_label, border_color=bg_color_dict[6])

        self.graph_1_table.add_component(graph_1)

    def select_from_platform_and_group(self, p: Platform):

        platform_objects = []
        for pg in self.platform_grades:
            if pg.platform.name == p.name:
                platform_objects.append(pg)
        print(platform_objects)
        # We assume here that we can not have more than one platform grade for user and platform
        platform_options = {str(plat_grade.id): str(plat_grade.user.name) for plat_grade in platform_objects}
        combo_groups = ComboBox(platform_options, lambda plat_grade_id: self.draw_graph_1(PlatformGrade.objects(
            id=plat_grade_id)[0]))
        self.graph_1_options_table.add_component(combo_groups, 0, 1)
        # Clear table

    def draw_graphs_table(self, group: Group):
        # Headers of Choosing table
        # graph_sp = StackPanel([])

        self.graph_1_table = StackPanel()
        self.layout_table.add_component(self.graph_1_table, 0, 0)
        # graph_sp.add_component(graph_1_table)
        graph_1_name = "ממוצע של צוער מול {0}".format(group.name)
        self.graph_1_table.add_component(Label(graph_1_name, size=SIZE_LARGE))

        # self.avg_grades_group = get_avg_of_platforms_by_group(group)

        graph_1_options_layout = GridPanel(2, 1)
        self.graph_1_table.add_component(graph_1_options_layout)
        graph_headers_1 = GridPanel(1, 2, bg_color=COLOR_PRIMARY_DARK)

        graph_1_options_layout.add_component(graph_headers_1, 0, 0)
        graph_headers_1.add_component(Label("פלטפורמה", fg_color='White'), 0, 0)
        graph_headers_1.add_component(Label("צוער", fg_color='White'), 0, 1)

        # self.layout_table.add_component(Label("cdfd"), 0, 0)

        # First combo_box
        self.graph_1_options_table = GridPanel(1, 2)
        graph_1_options_layout.add_component(self.graph_1_options_table, 1, 0)
        self.platform_grades, platform_options, counter_dict = get_major_platforms_of_group(group)
        self.avg_platforms_grade(counter_dict)

        combo_platform = ComboBox(platform_options, lambda p_id: self.select_from_platform_and_group(
            Platform.objects(id=p_id)[0]))
        self.graph_1_options_table.add_component(combo_platform, row=0, column=0)

    def select_mahzor(self, mahzor):
        # Shachar needs to complete
        group_name = "מחזור " + mahzor_num_to_letters[mahzor]
        print(group_name)
        group_objects =Group.objects(name__in=classes[mahzor]) #Group.objects(name=group_name)  #
        #print(group_objects)
        groups_options = {str(g.id): str(g.name) for g in group_objects}
        combo_groups = ComboBox(groups_options,
                                lambda g_id: self.draw_graphs_table(Group.objects(id=g_id)[0]))
        self.options_table.add_component(combo_groups, 0, 1)
        # Clear table
        self.layout_table.add_component(Label(""), 0, 0)

    def get_page_ui(self, user: User):
        self.user = user
        self.sp = StackPanel([])

        # Header
        self.title = Label("אזור הערכתי - מפקד/ת", size=SIZE_EXTRA_LARGE)
        self.sp.add_component(self.title)

        # Box of choosing
        options_layout = GridPanel(2, 1)
        self.sp.add_component(options_layout)

        # Headers of Choosing table
        self.options_headers = GridPanel(1, 2, bg_color=COLOR_PRIMARY_DARK)
        options_layout.add_component(self.options_headers, 0, 0)
        self.options_headers.add_component(Label("מחזור", fg_color='White'), 0, 0)
        self.options_headers.add_component(Label("קבוצה (מחלקה/צוות)", fg_color='White'), 0, 1)

        self.layout_table = GridPanel(1, 1)
        self.sp.add_component(self.layout_table)

        # First combo_box
        self.options_table = GridPanel(1, 2)
        options_layout.add_component(self.options_table, 1, 0)
        combo_machzor = ComboBox(mahzor_numstr_to_letters, lambda s: self.select_mahzor(int(s)))
        self.options_table.add_component(combo_machzor, row=0,
                                         column=0)

        group_search_box = ComboBox(self.mahzor_names, on_changed=lambda cadet: None)
        options_layout.add_component(group_search_box, 0, 1)
        # Second combo_box
        # groups_options = {str(g.id): str(g.name) for g in Group.objects(mahzor=user.mahzor)}
        # combo_groups = ComboBox(groups_options, lambda g_id: self.draw_graphs(Group.objects(id=g_id)[0]))
        # self.options_table.add_component(combo_groups, 0, 1)

        return self.sp
