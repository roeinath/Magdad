from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.components.chartjs_component import ChartjsComponent
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.getdata.academy_grades_interface import *
from typing import Dict
from web_features.Elements.personal_page.permissions import *
from web_framework.server_side.infastructure.constants import *


class GroupsGrades:
    def __init__(self, group, year, user):
        self.selected_group = group
        self.selected_year = year
        self.user = user

        self.gp = GridPanel(3, 1, bordered=False)
        self.gp.add_component(ChartjsComponent(height='15vw'), 2, 0)  # Patch

        options_layout = GridPanel(2, 1, bordered=False)
        options_layout.add_component(Label("בחר קורס", fg_color="black", bold=True), 0, 0)
        courses = {x: x for x in get_courses_list_for_group(self.selected_group, self.selected_year)}
        courses_combo = ComboBox(courses, self.load_grades)
        options_layout.add_component(courses_combo, 1, 0)
        self.gp.add_component(options_layout, 0, 0)

    def get_component(self):
        return self.gp

    def load_grades(self, course_name):
        course = get_single_course_of_group(self.selected_group, self.selected_year, is_user_captain(self.user),
                                            course_name)
        general_sp = StackPanel([])

        rolling_sum = 0

        grades_gp = GridPanel(course[0] + 3, 4)
        grades_gp.add_component(Label("צוער", size=SIZE_LARGE, fg_color="white"), row=0, column=0, column_span=2,
                                bg_color=COLOR_PRIMARY_DARK)
        grades_gp.add_component(Label("ציון סופי בקורס", size=SIZE_LARGE, fg_color="white"), row=0, column=2,
                                column_span=2,
                                bg_color=COLOR_PRIMARY_DARK)

        # TODO: grade_and_names better be dictionary
        grades_and_names = course[1:]

        names = [grade[0] for grade in grades_and_names]
        colors_dict_by_division = get_color_for_cadets_by_division(
            int(get_by_name_group(self.selected_group).group_tags[0]), names)

        cadets_colors_lst = colors_dict_by_division["cadets_colors_lst"]
        division_colors = colors_dict_by_division["divisions_colors_dict"]

        for i, grade in enumerate(grades_and_names):
            rolling_sum += grade[1]
            cadet_color = cadets_colors_lst[i]  # TODO Flato this is on you

            # name
            grades_gp.add_component(Label(grade[0]), row=i + 1, column=0, column_span=2, bg_color=cadet_color)

            # grade
            grades_gp.add_component(Label(grade[1]), row=i + 1, column=2, column_span=2, bg_color=cadet_color)

        # grid panel for colors of the divisions, to show what color is for each division
        if len(division_colors) != 0:
            gp_division_names = GridPanel(row_count=1, column_count=len(division_colors))
            i = 0
            for division_name, color in division_colors.items():
                gp_division_names.add_component(Label(division_name), bg_color=color, row=0, column=i)
                i += 1
            general_sp.add_component(gp_division_names)

        # add the components to the general grid panel

        self.load_histogram(course)
        self.gp.add_component(general_sp, 2, 0)

        general_sp.add_component(
            Label(text=f"ממוצע: {round(rolling_sum / course[0], 2)}", size=SIZE_LARGE))
        general_sp.add_component(gp_division_names)
        general_sp.add_component(grades_gp)

    def load_histogram(self, course_data):

        histo_graph = ChartjsComponent(width="40vw", height="25vw")
        buckets = [0] * 10
        bucket_labels = ["{0}-{1}".format(x, x + 9) for x in range(0, 90, 10)] + ["90-100"]
        for grade in course_data[1:]:
            for x in [i for i in range(0, 100, 10)]:
                if x <= grade[1] <= x + 9 and x != 90:
                    buckets[x // 10] += 1
                if x == 90 and grade[1] > 90:
                    buckets[9] += 1
        histo_graph.bar(bucket_labels, buckets, label="מספר צוערים", color=COLOR_PRIMARY_DARK,
                        border_color=COLOR_PRIMARY_DARK)
        self.gp.add_component(StackPanel([histo_graph], orientation=0), 1, 0)


class GroupSkira:

    def __init__(self, user, group, mahzor, year, sem):
        self.user = user
        self.group = group
        self.mahzor = mahzor
        self.year = year
        self.sem =sem
        self.graph_1_table = GridPanel(6, 1, bordered=False)
        self.platform = None

        # Defining our graphs
        self.graph_1_options_layout = GridPanel(2, 2, bordered=False)
        self.graph_1_table.add_component(self.graph_1_options_layout, 1, 0)
        self.graph_sp = StackPanel([ChartjsComponent(height="25vw")], orientation=VERTICAL)

        self.platform_grades, platform_options, counter_dict = get_major_platforms_of_group(group,year,sem)
        self.avg_platforms_grade(counter_dict)

        # Combo box
        self.graph_1_options_layout.add_component(Label("פלטפורמה", fg_color='black', bold=True), 0, 1)
        self.graph_1_options_layout.add_component(Label("צוער", fg_color='black', bold=True), 0, 0)

        combo_platform = ComboBox(platform_options, lambda p_id: self.select_from_platform_and_group(
            Platform.objects(id=p_id)[0]), default_value="מפקדים")

        # adding the graphs into the grid panel

        self.graph_1_options_layout.add_component(combo_platform, row=1, column=1)

        self.graph_1_options_layout.add_component(ComboBox({}, lambda s: None), 1, 0)

        self.graph_1_table.add_component(self.graph_sp, 2, 0)

    def select_from_platform_and_group(self, p: Platform):

        # getting the platforms_grade of platform using platform name
        platform_objects = []
        for pg in self.platform_grades:
            if pg.platform.name == p.name and pg.year == int(self.year) and pg.semester == self.sem:
                platform_objects.append(pg)


        # We assume here that we can not have more than one platform grade for user and platform
        self.platform = p
        name_options = {str(plat_grade.id): str(plat_grade.user.name) for plat_grade in platform_objects}
        combo_groups = ComboBox(name_options, lambda plat_grade_id: self.draw_radar_graphs(PlatformGrade.objects(
            id=plat_grade_id)[0], platform_objects))
        self.graph_1_options_layout.add_component(combo_groups, 1, 0)

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
                    # TODO: CHECK WHAT HAPPENED!
                    try:
                        self.avg_platforms_grades_of_group[pg_enc.platform][key] += pg_dec[key]
                    except:
                        pass
        for platform in self.avg_platforms_grades_of_group.keys():
            for key in self.avg_platforms_grades_of_group[platform].keys():
                self.avg_platforms_grades_of_group[platform][key] /= counter_dict[platform]

    def turn_grades_to_2list(self, dict: Dict):
        """

        :param dict: dict of params and grade [param,grad in param]
        :return: list of 2 dicts of the grades separated into Arachim and others
        """
        grades = [{}, {}]
        for key, val in dict.items():
            if "ערכים" in key:
                grades[1][key] = val
            else:
                grades[0][key] = val
        return grades

    def draw_radar_graphs(self, plat_grade: PlatformGrade, plat_grades):
        """
        Drawing our graphs!
        :param plat_grade: the platform grade for platform and user
        :param plat_grades: For future use! all the grades in the platform
        :return:
        """
        # Here we do some radar graphs - for ARACHIM and the second for the opther parameters
        self.graph_sp.clear()
        avg_grades_platform = self.turn_grades_to_2list(self.avg_platforms_grades_of_group[plat_grade.platform])
        grades = self.turn_grades_to_2list(plat_grade.decrypted_grades(is_real_data=is_user_captain(self.user)))

        # First radar graph
        graph_label = "ציון - {0}".format(plat_grade.user.name)
        graph_1 = ChartjsComponent(width="25vw", height="25vw")
        graph_1.labels('r', size=10)
        graph_1.title("מקצועיות ומנהיגות", size=25)
        graph_1.legend(size=15)
        description = [PARAM_DICT[a] for a in avg_grades_platform[0].keys()]  # list(filter(lambda key:
        avg_grade = [val if val >= 1 else 0 for val in
                     avg_grades_platform[0].values()]  # list(filter(lambda val: val >= 1,avg_grades_platform.values()))
        graph_1.radar(description, avg_grade, label="ממוצע של {}".format(self.group.name),
                      border_color=bg_color_dict[1])
        single_grade = grades[0].values()  # list(filter(lambda val: val >= 1, grades.values()))
        graph_1.scale('r', min=0, max=max(6, max(avg_grade), max(single_grade)))
        graph_1.radar(description, single_grade, label=graph_label, border_color=bg_color_dict[6])

        # Second radar graph
        graph_2 = ChartjsComponent(width="25vw", height="25vw")
        graph_2.labels('r', size=10)
        graph_2.title("ערכים", size=25)
        graph_2.legend(size=15)
        description_2 = [PARAM_DICT[a] for a in avg_grades_platform[1].keys()]  # list(filter(lambda key:
        avg_grade_2 = [val if val >= 1 else 0 for val in avg_grades_platform[1].values()]
        # list(filter(lambda val: val >= 1,avg_grades_platform.values()))
        graph_2.radar(description_2, avg_grade_2, label="ממוצע של {}".format(self.group.name),
                      border_color=bg_color_dict[1])
        single_grade_2 = grades[1].values()  # list(filter(lambda val: val >= 1, grades.values()))
        graph_2.scale('r', min=0, max=max(3, max(single_grade_2), max(avg_grade_2)))
        graph_2.radar(description_2, single_grade_2, label=graph_label, border_color=bg_color_dict[6])

        # Third graph - scatter
        graph_3 = ChartjsComponent(width="25vw", height="25vw")
        graph_3.title("השוואת פרמטרים - בקרוב!", size=25)
        # Adding the graphs to stack panel
        self.graph_sp.add_component(StackPanel([graph_1, graph_2], orientation=0))
        self.graph_sp.add_component(graph_3)

    def get_component(self):
        return self.graph_1_table


class CompareStats:
    def __init__(self, user, group_name, year):
        self.user = user
        self.gp = GridPanel(3, 1)
        group = get_by_name_group(group_name)
        options_layout = GridPanel(4, 2, bg_color=COLOR_PRIMARY_DARK)
        platforms_list = PlatformGrade.objects(user__in=group.participants).select_related(1)
        platforms_options = {x.platform.name: x.platform.name for x in platforms_list}
        platforms_options["ממוצע - אקדמיה"] = "ממוצע - אקדמיה"

        self.main_x_combo = ComboBox(platforms_options, self.x_main_changed)
        self.main_y_combo = ComboBox(platforms_options, self.y_main_changed)
        self.sec_x_combo = ComboBox({}, None)
        self.sec_y_combo = ComboBox({}, None)
        self.load_button = Button("טען גרף", self.load_graph)

        options_layout.add_component(Label("פרמטר ציר x"), row=0, column=0)
        options_layout.add_component(Label("פרמטר ציר y"), row=0, column=1)
        options_layout.add_component(self.main_x_combo, row=1, column=0)
        options_layout.add_component(self.main_y_combo, row=1, column=1)
        options_layout.add_component(self.sec_x_combo, row=2, column=0)
        options_layout.add_component(self.sec_y_combo, row=2, column=1)
        options_layout.add_component(self.load_button, row=3, column=0, column_span=2)

        self.gp.add_component(options_layout, 0, 0)

    def get_component(self):
        return self.gp

    def x_main_changed(self, plat):
        if plat != "ממוצע - אקדמיה":
            self.sec_x_combo = ComboBox()

    def y_main_changed(self, plat):
        pass

    def load_graph(self):
        pass
