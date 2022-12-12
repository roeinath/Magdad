from APIs.TalpiotAPIs.AssessmentAPI.Database.files import Files
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.confirmation_button import ConfirmationButton
from web_framework.server_side.infastructure.components.display_google_docs_file import GoogleDocsDisplay
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.getdata.academy_grades_interface import *
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.getdata.skirot_grades_interface import *
from web_framework.server_side.infastructure.components.chartjs_component import ChartjsComponent
from web_features.Elements.personal_page.modules.constants import *
import math
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_features.Elements.personal_page.modules.grades_from_moodle import *
from APIs.TalpiotAPIs.AssessmentAPI.tsyunomat.GetDataFromDB import *
from os import chdir
from os.path import abspath, dirname
from web_features.Elements.personal_page.permissions import is_user_captain
SIZE_EXTRA_SMALL = 'xs'
SIZE_SMALL = 'sm'
SIZE_MEDIUM = 'md'
SIZE_LARGE = 'lg'
SIZE_EXTRA_LARGE = 'xl'


class CadetGrades:
    def __init__(self, user: User, year: int, cadet: str, is_real_data: bool):
        self.user: User = user
        self.year: int = year
        self.cadet: str = cadet
        self.is_real_data: bool = is_real_data  # whether getting the real or the fake data

        self.grades_layout: GridPanel = None
        self.popup: PopUp = None

    def user_is_not_cadet(self):
        if is_user_X_admin(self.user):
            return True
        elif is_user_captain(self.user):
            return True
        return False

    def get_ui(self):
        self.grades_layout = GridPanel(3, 1, bordered=False)
        self.grades_layout.add_component(self.get_table(), 0, 0)
        if self.user_is_not_cadet():
            self.grades_layout.add_component(Button("הוספת ציון", self.edit_grade_popup), 1, 0)
        return self.grades_layout

    def edit_grade_popup(self, current_grade: CourseGrade = None):
        def edit_grade(course_grade: CourseGrade):
            course_grade.user = User.objects(name=self.cadet).first()
            course_grade.year = self.year
            course_grade.is_real_data = self.is_real_data
            course_grade.grade = CourseGrade.encrypt(course_grade.grade)
            course_grade.save()
            print(course_grade)
            self.popup.hide()

        print(current_grade)

        form = JsonSchemaForm(
            CourseGrade,
            value=current_grade,
            visible=['course', 'grade', 'moed', 'semester'],
            not_editable=['course'] if current_grade is not None else [],
            display_name={'course': 'שם הקורס', 'grade': 'ציון', 'moed': 'מועד', 'semester': 'סמסטר'},
            options={'course': Course.objects, 'moed': ["A", "B"], 'semester': ["A", "B", "A+B"]},
            options_display={'course': lambda x: str(x), 'moed': lambda x: x, 'semester': lambda x: x},
            submit=edit_grade
        )

        if self.user_is_not_cadet():
            popup_component = form
        else:
            popup_component = Label("אין אפשרות לערוך את הציון", fg_color='red')

        self.popup = PopUp(popup_component, title="עריכת ציון", is_shown=True, is_cancelable=True)
        self.grades_layout.add_component(self.popup, 2, 0)

    def delete_grade(self, current_grade: CourseGrade):
        current_grade.delete()

    def get_table(self):
        """
        pulls the grades and puts them in a table
        :return: GridPanel with grades
        """
        grades, average = get_courses_of_user(self.cadet, self.year, self.is_real_data)

        sort_by_semester = lambda v: v[1]["semester"] if v[1]["semester"] is not None else "A+B"
        grades = {k: v for k, v in sorted(grades.items(), key=sort_by_semester)}  # sorting by semester

        grades_gp = GridPanel(len(grades) + 4, 6)
        grades_gp.add_component(Label("קורס", size=SIZE_LARGE, fg_color="white"), row=0, column=4,
                                bg_color=COLOR_PRIMARY_DARK)
        grades_gp.add_component(Label("ציון", size=SIZE_LARGE, fg_color="white"), row=0, column=3,
                                bg_color=COLOR_PRIMARY_DARK)
        grades_gp.add_component(Label('נ"ז', size=SIZE_LARGE, fg_color="white"), row=0, column=2,
                                bg_color=COLOR_PRIMARY_DARK)
        grades_gp.add_component(Label("סמסטר", size=SIZE_LARGE, fg_color="white"), row=0, column=1,
                                bg_color=COLOR_PRIMARY_DARK)
        grades_gp.add_component(Label("מועד", size=SIZE_LARGE, fg_color="white"), row=0, column=0,
                                bg_color=COLOR_PRIMARY_DARK)

        if self.user_is_not_cadet():
            grades_gp.add_component(Label("", size=SIZE_LARGE, fg_color="white"), row=0, column=5,
                                    bg_color=COLOR_PRIMARY_DARK)

        if grades == {} and average == -1:
            grades_gp.add_component(Label("אין מידע רלוונטי כרגע", bold=True, size=SIZE_LARGE), row=2, column=3,
                                    column_span=5)
            return grades_gp

        grades_gp.add_component(Label("ממוצע", bold=True), row=1, column=4)
        bg_color = bg_color_of_courses(average)
        grades_gp.add_component(Label(str(round(average, 2)), bold=True), row=1, column=0, column_span=4,
                                bg_color=bg_color)

        courses_dict = {}
        for course in Course.objects:
            courses_dict[course.name] = course

        i = 2
        for course_name, course_grade in grades.items():
            grades_gp.add_component(Label(text=str(course_name)), row=i, column=4)
            grades_gp.add_component(Label(text=str(course_grade["credits"])), row=i, column=2)
            grades_gp.add_component(Label(text=str(course_grade["semester"])), row=i, column=1)
            if course_grade["semester"] == "A+B":
                grades_gp.add_component(Label(text="לא ידוע"), row=i, column=1)
            grades_gp.add_component(Label(text=str(course_grade["moed"])), row=i, column=0)
            if course_grade["grade"] == course_grade["moed_a_grade"]:
                grades_gp.add_component(Label(text="לא ידוע"), row=i, column=0)
            # print(course_grade["grade"],course_grade["moed_a_grade"],course_grade["moed"])
            bg_color = bg_color_of_courses(course_grade["grade"])
            if course_grade["grade"] == -1:
                grades_gp.add_component(Label(text="לא קיבל ציון/פטור"), row=i, column=3)
            elif course_grade["moed_a_grade"] != -1 and course_grade["moed"] == "B":
                grades_gp.add_component(
                    Label(text="{0} ({1})".format((course_grade["grade"]), str(course_grade["moed_a_grade"]))), row=i,
                    column=3, bg_color=bg_color)
            elif math.floor(course_grade["grade"]) == course_grade["grade"]:
                grades_gp.add_component(Label(text=str(int(course_grade["grade"]))), row=i, column=3, bg_color=bg_color)
            else:
                grades_gp.add_component(Label(text=str(round(course_grade["grade"], 2))), row=i, column=3,
                                        bg_color=bg_color)

            if self.user_is_not_cadet():
                course_grade_item: CourseGrade = CourseGrade.objects(user=User.objects(name=self.cadet).first(),
                                                                     course=courses_dict[course_name]).first()
                if course_grade_item is not None:
                    course_grade_item.grade = str(CourseGrade.decrypt(course_grade_item.grade))
                    sp = StackPanel([
                        Button("עריכה", lambda grade=course_grade_item: self.edit_grade_popup(grade)),
                        ConfirmationButton("מחיקה", lambda g=course_grade_item: self.delete_grade(g), bg_color='red')
                    ])
                    grades_gp.add_component(sp, row=i, column=5)
            i += 1

        return grades_gp


class CadetSkira:
    def __init__(self, user, year, cadet, is_real_data):
        self.user = user
        self.year = year
        self.cadet = cadet
        # temporary, needs to replace self.cadet
        self.cadet_user = User.objects.filter(name=self.cadet).first()
        self.is_real_data = is_real_data

    def get_table(self):  # TODO way too long of a function!!
        self.grades_sp = StackPanel()

        platforms_dict = get_skira_of_user(self.cadet, is_real_data=self.is_real_data)
        platforms_dict_by_sem = platforms_dict_by_semester(platforms_dict)
        # filters according to relevant year
        relevant = {key: val for key, val in platforms_dict_by_sem.items() if key[0] == self.year}
        # lists for Accordion
        platforms = []  # the names of the platforms
        tables = []  # tables components
        docs_url = []  # urls to the docs
        counter = 2
        for time, platforms_dict_sem in relevant.items():
            # TODO: generalize the number of grades
            avg_grades_sem = [{},
                              {}]  # seperate dicts for arachim and not arachim. keys are parameter name, values are grade.
            avg_grades_sem_self = [{}, {}]
            avg_grades_sem_friends = [{}, {}]
            gr_sem = StackPanel([], orientation=0)
            platform_grid_table = GridPanel(4 + len(platforms_dict_sem.keys()), GRADES, bordered=True,
                                            bg_color=COLOR_PRIMARY_DARK)
            platform_grid_table.add_component(
                Label(SEMESTER + " {0} -{1}".format(semester_dict[time[1]], time[0]), size=SIZE_MEDIUM,
                      fg_color='White', italic=True), 0, 0)
            platform_grid_table.add_component(Label(""), 1, 0)

            for j, (platform, info) in enumerate(platforms_dict_sem.items()):
                if platform != COUNT:
                    # the table for each semester
                    # add the grades in the stack panel
                    platform_grid_table.add_component(Label(platform, fg_color='White', italic=True, size=13), j + 1, 0)
                    items = list(PARAM_DICT.keys())
                    for i in range(len(items)):
                        description = items[i]
                        grade = info["grades"][description]
                        if counter == 2:
                            # TODO : generalize the grade description row
                            if i == 0:
                                platform_grid_table.add_component(Label(LEADERSHIP, size=SIZE_LARGE,
                                                                        fg_color='White', italic=True), 0,
                                                                  i + 1, column_span=3)
                            if i == 3:
                                platform_grid_table.add_component(Label(professionalism, size=SIZE_LARGE,
                                                                        fg_color='White', italic=True), 0,
                                                                  i + 1, column_span=4)
                            if i == 7:
                                platform_grid_table.add_component(Label(ARACHIM, size=SIZE_LARGE,
                                                                        fg_color='White', italic=True), 0,
                                                                  i + 1, column_span=6)
                            platform_grid_table.add_component(Label(PARAM_DICT[description], size=13,
                                                                    fg_color='White', italic=True), 1,
                                                              i + 1)

                        if grade == 0:
                            platform_grid_table.add_component(Label(), counter, i + 1, bg_color='Black')
                        else:
                            if platform == "סטיית תקן":
                                platform_grid_table.add_component(Label("{:.2f}".format(grade), fg_color='White'),
                                                                  counter, i + 1,
                                                                  bg_color=bg_color_of_grade(grade, description,
                                                                                             platform))
                            grade_new = grade / platforms_dict_sem[COUNT]["grades"][
                                description] if platform == AVG else grade
                            if math.floor(grade_new) == grade_new:
                                platform_grid_table.add_component(Label("{:.0f}".format(grade_new), fg_color='White'),
                                                                  counter, i + 1,
                                                                  bg_color=bg_color_of_grade(grade_new, description,
                                                                                             platform))
                            else:
                                platform_grid_table.add_component(Label("{:.2f}".format(grade_new), fg_color='White'),
                                                                  counter, i + 1,
                                                                  bg_color=bg_color_of_grade(grade_new, description,
                                                                                             platform))
                            if "ערכים" in description:
                                ARACHIM_flag = 1
                            else:
                                ARACHIM_flag = 0
                            if platform == "מפקדים":
                                avg_grades_sem[ARACHIM_flag][PARAM_DICT[description]] = grade_new
                            if platform == "הערכה עצמית" or platform == "עצמית":
                                avg_grades_sem_self[ARACHIM_flag][PARAM_DICT[description]] = grade_new
                            if platform == "סוציומטרי":
                                avg_grades_sem_friends[ARACHIM_flag][PARAM_DICT[description]] = grade_new

                    counter += 1
            graph_panel = StackPanel([], orientation=0)

            if avg_grades_sem[0] or avg_grades_sem_self[0] or avg_grades_sem_friends[0]:
                chart_1 = ChartjsComponent(width="20vw", height="20vw")
                chart_1.scale('r', min=0, max=6)
                chart_1.legend(size=15)
                chart_1.labels('r', size=15)
                chart_1.title("תמונת {0}-{1}".format(professionalism, LEADERSHIP), size=17)

            if avg_grades_sem[0]:
                chart_1.radar(list(avg_grades_sem[0].keys()), list(avg_grades_sem[0].values()), label="מפקדים",
                              border_color=bg_color_dict[6])
            if avg_grades_sem_self[0]:
                chart_1.radar(list(avg_grades_sem_self[0].keys()), list(avg_grades_sem_self[0].values()),
                              label="הערכה עצמית", border_color=bg_color_dict[3])
            if avg_grades_sem_friends[0]:
                chart_1.radar(list(avg_grades_sem_friends[0].keys()), list(avg_grades_sem_friends[0].values()),
                              label="סוציומטרי", border_color=bg_color_dict[1])

            if avg_grades_sem[1] or avg_grades_sem_self[1] or avg_grades_sem_friends[1]:
                chart_2 = ChartjsComponent(width="20vw", height="20vw")
                chart_2.scale('r', min=0, max=3)
                chart_2.labels('r', size=15)
                chart_2.title("מצפן ערכי", size=17)
                chart_2.legend(size=15)

            if avg_grades_sem[1]:
                chart_2.radar(list(avg_grades_sem[1].keys()), list(avg_grades_sem[1].values()), label="מפקדים",
                              border_color=bg_color_dict[6])
            if avg_grades_sem_self[1]:
                chart_2.radar(list(avg_grades_sem_self[1].keys()), list(avg_grades_sem_self[1].values()),
                              label="הערכה עצמית", border_color=bg_color_dict[3])
            if avg_grades_sem_friends[1]:
                chart_2.radar(list(avg_grades_sem_friends[1].keys()), list(avg_grades_sem_friends[1].values()),
                              label="סוציומטרי", border_color=bg_color_dict[1])

            if avg_grades_sem[0] or avg_grades_sem_self[0] or avg_grades_sem_friends[0]:
                graph_panel.add_component(chart_1)
            if avg_grades_sem[1] or avg_grades_sem_self[1] or avg_grades_sem_friends[1]:
                graph_panel.add_component(chart_2)

            # add the content and the title to their lists
            # add skira
            print(self.cadet)
            doc_url = get_docs_by_user(self.cadet_user, time[1], self.year)
            print(doc_url, time[1], self.cadet_user, self.year)
            if doc_url is None:
                docs_url.append(None)
            else:
                docs_url.append(GoogleDocsDisplay(doc_url))
            gr_sem.add_component(platform_grid_table)
            gr_sem.add_component(graph_panel)
            tables.append(gr_sem)
            platforms.append(SEMESTER + " {0}-{1}".format(semester_dict[time[1]], time[0]))
            counter = 2

        # draw all of the tables
        for i in range(len(relevant.keys())):
            self.grades_sp.add_component(Label(platforms[i], bold=True, size=SIZE_EXTRA_LARGE))
            if docs_url[i] is not None:
                self.grades_sp.add_component(docs_url[i])
            self.grades_sp.add_component(tables[i])

        return self.grades_sp


def moodle_login(user):
    '''
    :param user: name of the user we want to find grades of
    :return: grades of exercises of user
    '''
    moodle = MoodleAPI()
    info = get_specific_user_info(user)
    if info == None:
        return None
    mail = info['email']
    password = info['password']
    moodle.initialise(mail, password)
    chdir(dirname(abspath(__file__)))
    courses = moodle.get_courses()
    grades = moodle.get_grades(courses)
    return grades


class CadetExGrades:
    def __init__(self, user, year, cadet):
        self.user = user
        self.year = year
        self.cadet = cadet

    def get_table(self):
        '''
        gets grades for excercises from moodle and returns sliders for every course
        that opens table with exercise names and grades
        '''
        total_gp = GridPanel(1, 1, bordered=False)
        grades = moodle_login(self.cadet)  # gets dict of {course_num : {exc_name : grade}}
        if grades == None:
            total_gp.add_component(Label("אין ציונים"), 0, 0)
            return total_gp
        course_names = get_name_course_by_number(grades)  # dict of {course_num : course_name}
        inner_gp = GridPanel(len(grades), 1, bordered=False)
        j = 0
        for course in grades:
            if course_names[str(course)] != None:  # if there is a name for course in DB, change it
                course_name = course_names[str(course)]
            else:
                course_name = course

            course_gp = GridPanel(1, 1, bordered=False)
            grades_gp = GridPanel(len(grades[course]), 2)
            grades_gp.add_component(Label("משימה", size=SIZE_LARGE, fg_color="white"), row=0, column=1,
                                    bg_color=COLOR_PRIMARY_DARK)
            grades_gp.add_component(Label("ציון", size=SIZE_LARGE, fg_color="white"), row=0, column=0,
                                    bg_color=COLOR_PRIMARY_DARK)

            i = 1
            for exr in grades[course]:
                grades_gp.add_component(Label(text=str(exr)), row=i, column=1)
                grades_gp.add_component(Label(text=str(grades[course][exr])), row=i, column=0)
                i += 1

            course_gp.add_component(Accordion([grades_gp], [course_name], size=SIZE_MEDIUM), 0, 0)
            inner_gp.add_component(course_gp, j, 0)
            j += 1

        total_gp.add_component(Accordion([inner_gp], ["תרגילים"], size=SIZE_LARGE), 0, 0)
        return total_gp


def get_docs_by_user(us, sem, year):
    file = Files.objects.filter(user=us)
    revelant_sem = chr(ord(list(sem)[0]) + 2 * mahzor_number_to_years[us.mahzor].index(year))
    # print(revelant_sem, sem, year, us.mahzor)
    if len(file) > 0:
        # print("list of urls: of {0} and sem = {1}".format(us.name, revelant_sem), list(file[0].skirot_url))
        if revelant_sem in list(file[0].skirot_url):
            url = file[0].skirot_url[revelant_sem]
            # print("url sem {} ".format(revelant_sem), url)
            if url == "None":
                return None
            return url
    return None
