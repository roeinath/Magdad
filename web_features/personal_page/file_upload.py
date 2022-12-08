import math
import os

from web_framework.server_side.infastructure.components.confirmation_button import ConfirmationButton
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.upload_files import UploadFiles
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.page import Page
from APIs.ExternalAPIs.GoogleDrive.file_to_upload import FileToUpload
from web_features.personal_page.permissions import *
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.getdata.academy_grades_interface import *
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.uploaddata.skirot_presubmit import basic_processing
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.uploaddata.find_skirot_data import find
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.uploaddata.upload_skirot_data import upload_platforms
from functools import partial
from APIs.TalpiotSystem import TalpiotSettings
from web_framework.server_side.infastructure.constants import *

RealData = TalpiotSettings.is_master()  # true iff we are on master

PARAM_DICT = {"דמות (מנהיגות)": "דמות", "תפקוד בחברה (מנהיגות)": "תפקוד בחברה", "הובלה (מנהיגות)": "הובלה",
              "ניהול (מקצועיות)": "ניהול", "מדעי אקדמי (מקצועיות)": "מדעי אקדמי", "מדעי יישומי (מקצועיות)": "מדעי "
                                                                                                            "יישומי",
              "בטחוני (מקצועיות)": "בטחוני", "א (ערכים)": "אחריות", "ד (ערכים)": "דרך ארץ", "ה (ערכים)": "העזה",
              "י (ערכים)": "יושרה",
              "מ (ערכים)": "מצוינות", "ש (ערכים)": "שליחות"}
ARACHIM = "ערכים"
LEADERSHIP = "מנהיגות"
professionalism = "מקצועיות"


class FileUpload(Page):
    def __init__(self, params):
        super().__init__(params)
        self.is_real_data = RealData
        self.gp = None
        self.mahzor_names = {}
        self.selected_year = None
        self.selected_mahzor = None
        self.selected_cadet = None
        self.selected_sem = None
        self.selected_document_type = None
        self.popup = None
        self.update = "n"
        self.user_options = None

    @staticmethod
    def get_title():
        return "העלאת משובים"

    @staticmethod
    def is_authorized(user):
        return MATLAM in user.role  # Only the people of the base

    @staticmethod
    def get_group(user):  # TODO Need more informative name or comment
        if is_user_captain(user) or (is_user_X_admin(user) and not RealData):
            return "All"
        if is_user_sagaz(user):
            return get_team_of_sagaz(user) + [user]
        if is_user_cadet(user):
            return [user]

    @staticmethod
    def format_grades(text_dic, platforms):
        rez = ""
        for i, plat in enumerate(platforms):
            row = ""
            p = plat[0]
            row += f"{p} ||  "
            for grade in text_dic[i].items():
                row += f"{grade[0].split('(')[0]}: {grade[1]} | "
            rez += row + "\n"
        return rez

    def upload(self, files):
        """
        The main function in this file. Carries the whole operation of file uploading, using the other functions and
        scripts
        :param files: this function originally worked for whole folders, and that's why files is an iterable.
        the function can still work inside a for loop, iterating on files
        """
        print(f"Cadet: {self.selected_cadet} | Year: {self.selected_year} | Mahzor: {self.selected_mahzor} | Semester: "
              f"{self.selected_sem}")
        f = FileToUpload.load_from_json(files[0])
        with open(f.name, 'wb') as g:
            # Saving the uploaded file on the server (the Azure), Only for a short time
            g.write(f.get_content())

        rez = basic_processing(self.selected_cadet, self.selected_year, self.selected_mahzor, f.name)
        # A function which runs the presubmit checks on the uploaded file, and returns None\ Error message

        if rez:
            # Presubmit failed
            self.message(rez, 'שגיאה בפורמט הקובץ')

        else:
            # Successfully presubmit
            name, text, platforms, find_error = find(f.name, self.selected_cadet)
            # A function for getting the grades from the file
            if find_error:
                # An error was found while parsing the grades out of the file
                self.message(find_error, 'שגיאה בפורמט הקובץ')

            else:
                # All tests passed, uploading the found grades
                worked, upload_rez = upload_platforms(name, text, platforms, mahzor=self.selected_mahzor,
                                                      year=self.selected_year, semester=self.selected_sem,
                                                      is_real_data=self.is_real_data, update=self.update)

                if not worked:
                    self.message(upload_rez, "שגיאה בהעלאת הקובץ")
                if worked:
                    self.message("ההעלאה הסתיימה בהצלחה!", "הצלחה!")

        os.remove(f.name)
        # Deleting the file from the Azure
        self.change_cadet(self.selected_cadet)

    def message(self, text, title):
        self.popup = PopUp(Label(text), title=title, is_shown=True, is_cancelable=True)
        self.gp.add_component(self.popup)

    # TODO: fix this page_ui with default values
    # def get_page_ui(self, user: User):
    #     """
    #     returns the page's main UI component (grid panel)
    #     """
    #     self.user = user
    #
    #     self.gp = GridPanel(5, 3, bordered=False)
    #
    #     # Header
    #     self.gp.add_component(Label("העלאת משובים", size=SIZE_EXTRA_LARGE), 0, 0)
    #
    #     self.options_layout = GridPanel(2, 5, bg_color=COLOR_PRIMARY_DARK)
    #
    #     # Labels
    #     self.options_layout.add_component(Label("מצב", fg_color='White'), 0, 4)
    #     self.options_layout.add_component(Label("מחזור", fg_color='White'), 0, 3)
    #     self.options_layout.add_component(Label("צוער", fg_color='White'), 0, 2)
    #     self.options_layout.add_component(Label("שנה", fg_color='White'), 0, 1)
    #     self.options_layout.add_component(Label("סמסטר", fg_color='White'), 0, 0)
    #
    #     # Options
    #     self.mode_combo = ComboBox({"y": "עדכון", "n": "העלאה"},
    #                                on_changed=lambda mode: self.change_mode(mode), default_value="n")
    #     self.options_layout.add_component(self.mode_combo, 1, 4)
    #     if is_user_captain(self.user):
    #         x =  CommandedGroup.objects(commander=user).select_related(1)
    #         if x is not None:
    #             self.selected_mahzor =x[0].participants[0].mazhor
    #         else:
    #             self.selected_mahzor = "43"
    #     else:
    #         self.selected_mahzor = self.user.mahzor
    #     self.mahzor_combo = ComboBox({"43": "מג", "42": "מב", "41": "מא"},
    #                                  on_changed=lambda selected_mahzor: self.load_cadet_search_box(selected_mahzor),
    #                                  default_value=str(self.selected_mahzor))
    #     self.options_layout.add_component(self.mahzor_combo, 1, 3)
    #     if is_user_captain(self.user):
    #         user_options = {str(u.name): str(u.name) for u in User.objects(mahzor=self.selected_mahzor)}
    #         self.cadet_search_box = ComboBox(user_options, on_changed=lambda cadet: self.change_cadet(cadet))
    #
    #     else:
    #         user_options = {str(u.name): str(u.name) for u in User.objects(name=user.name)}
    #         self.cadet_search_box = ComboBox(user_options, on_changed=lambda cadet: self.change_cadet(cadet),
    #                                          default_value=self.user.name)
    #         self.options_layout.add_component(self.cadet_search_box, 1, 2)
    #
    #     self.year_combo = ComboBox({year: year for year in ["2022", "2021", "2020"]},
    #                                on_changed=lambda year: self.change_year(year))
    #     self.options_layout.add_component(self.year_combo, 1, 1)
    #
    #     self.semester_combo = ComboBox({"A": "א'", "B": "ב'"},
    #                                    on_changed=lambda sem: self.change_sem(sem))
    #     self.options_layout.add_component(self.semester_combo, 1, 0)
    #
    #     self.gp.add_component(self.options_layout, 1, 0)
    #
    #     if not is_user_captain(self.user):
    #         self.change_cadet(self.user.name)
    #     print(f"Is the data real? {RealData}")
    #     return self.gp

    def get_page_ui(self, user: User):
        """
        returns the page's main UI component (grid panel)
        """
        self.user = user

        self.gp = GridPanel(5, 3, bordered=False)

        # Header
        self.gp.add_component(Label("העלאת משובים", size=SIZE_EXTRA_LARGE), 0, 0)

        self.options_layout = GridPanel(2, 5, bg_color=COLOR_PRIMARY_DARK)

        # Labels
        self.options_layout.add_component(Label("מצב", fg_color='White'), 0, 4)
        self.options_layout.add_component(Label("מחזור", fg_color='White'), 0, 3)
        self.options_layout.add_component(Label("צוער", fg_color='White'), 0, 2)
        self.options_layout.add_component(Label("שנה", fg_color='White'), 0, 1)
        self.options_layout.add_component(Label("סמסטר", fg_color='White'), 0, 0)

        # Options
        self.mode_combo = ComboBox({"y": "עדכון", "n": "העלאה"},
                                   on_changed=lambda mode: self.change_mode(mode), default_value="n")
        self.options_layout.add_component(self.mode_combo, 1, 4)
        if is_user_captain(self.user):
            self.selected_mahzor = 43
        else:
            self.selected_mahzor = self.user.mahzor
        self.mahzor_combo = ComboBox({"44": "מד","43": "מג", "42": "מב"},
                                     on_changed=lambda selected_mahzor: self.load_cadet_search_box(selected_mahzor),
                                     default_value=str(self.selected_mahzor))
        self.options_layout.add_component(self.mahzor_combo, 1, 3)
        if is_user_captain(self.user):
            self.user_options = {str(u.name): str(u.name) for u in User.objects(mahzor=self.selected_mahzor)}
        else:
            self.user_options = {str(u.name): str(u.name) for u in User.objects(name=user.name)}

        self.cadet_search_box = ComboBox(self.user_options, on_changed=lambda cadet: self.change_cadet(cadet))
        self.options_layout.add_component(self.cadet_search_box, 1, 2)

        self.year_combo = ComboBox({year: year for year in ["2022", "2021", "2020"]},
                                   on_changed=lambda year: self.change_year(year))
        self.options_layout.add_component(self.year_combo, 1, 1)

        self.semester_combo = ComboBox({"A": "א'", "B": "ב'"},
                                       on_changed=lambda sem: self.change_sem(sem))
        self.options_layout.add_component(self.semester_combo, 1, 0)

        self.gp.add_component(self.options_layout, 1, 0)

        # if not is_user_captain(self.user):
        #     self.change_cadet(self.user.name)

        print(f"Is the data real? {RealData}")
        return self.gp

    def load_cadet_search_box(self, m):
        """
        runs when a mahzor is chosen. loads all names of cadets from the chosen mahzor.
        :param m: string of mahzor's number
        :return None
        """
        self.selected_mahzor = int(m)

        group = self.get_group(self.user)
        print(group)
        self.mahzor_names = {}
        print([user.name for user in User.objects(mahzor=self.selected_mahzor)])
        for cadet in User.objects(mahzor=self.selected_mahzor):
            if group == "All" or cadet in group:
                cadet_name = cadet.name
                self.mahzor_names[cadet_name] = cadet_name

        self.cadet_search_box = ComboBox(self.mahzor_names,
                                         on_changed=lambda cadet: self.change_cadet(cadet))

        self.options_layout.add_component(self.cadet_search_box, 1, 2)
        self.check_if_ready()

    def get_user_n_platforms(self):
        """
        A function for getting the number of platform grades of a given user
        :return: the number
        """
        user = User.objects.filter(name=self.selected_cadet).first()
        plats = PlatformGrade.objects.filter(user=user, is_real_data=self.is_real_data)
        return len(plats)

    def delete_grade(self, platform):
        """
        A function for deleting a platform grade when the delete button is pressed
        :param platform: the platform id to be deleted
        """
        print(f"Deleting {platform} Grade")
        plat = PlatformGrade.objects.filter(id=platform, is_real_data=self.is_real_data).first()
        try:
            plat.delete()
        except:
            pass
        self.change_cadet(self.selected_cadet)

    def get_cadet_grades(self, cadet):
        """
        A function for getting the data to show in the grades table
        :return: the data for the table
        """
        user = User.objects.filter(name=cadet).first()
        grades = PlatformGrade.objects.filter(user=user, is_real_data=self.is_real_data)
        platform_grades = []
        names = []
        ids = []
        semesters = []
        years = []
        for g in grades:
            semesters.append(g.semester)
            years.append(g.year)
            names.append(g.platform.name)
            single_plat = g.decrypted_grades(is_real_data=True)
            platform_grades += [single_plat]
            ids.append(g.id)
        return platform_grades, names, ids, semesters, years

    def change_cadet(self, cadet):
        """
        A function for creating the UI of the grades table.
        :param cadet:
        :return:
        """
        self.selected_cadet = cadet
        self.table = GridPanel(self.get_user_n_platforms() + 3, 17, bg_color=COLOR_PRIMARY_DARK)
        self.table.add_component(Label(f"ציוני הפלטפורמות של {cadet}", fg_color='White'), 0, 0, column_span=17)
        grades, names, ids, semesters, years = self.get_cadet_grades(cadet)
        if names:
            # add the titles
            fields = [""] + list(PARAM_DICT.values()) + ["סמסטר", "שנה", ""]
            # print(fields)
            for index, f in enumerate(fields):
                if index == 0:
                    self.table.add_component(Label(""), 1,
                                             0, column_span=1)
                    self.table.add_component(Label(LEADERSHIP, size=SIZE_LARGE,
                                                   fg_color='White', italic=True), 1,
                                             index + 1, column_span=3)
                if index == 3:
                    self.table.add_component(Label(professionalism, size=SIZE_LARGE,
                                                   fg_color='White', italic=True), 1,
                                             index + 1, column_span=4)
                if index == 7:
                    self.table.add_component(Label(ARACHIM, size=SIZE_LARGE,
                                                   fg_color='White', italic=True), 1,
                                             index + 1, column_span=6)
                    self.table.add_component(Label(""), 1,
                                             14, column_span=3)
                self.table.add_component(Label(f, fg_color='White'), row=2, column=index)
            # add the delete buttons
            for index, n in enumerate(names):
                self.table.add_component(Label(n, fg_color='White'), row=index + 3, column=16)
                self.table.add_component(ConfirmationButton(text="מחק", fg_color='White', action=partial(
                    self.delete_grade, ids[index])), index + 3, 0)
            # print(grades)
            for i, platform in enumerate(grades):
                # add semesters and years
                self.table.add_component(Label(str(years[i]), fg_color='White'), row=i + 3, column=15)
                self.table.add_component(Label(str(semesters[i]), fg_color='White'), row=i + 3, column=14)
                # add the platform grades
                print(platform)
                for j, grade in enumerate(platform):
                    print(grade)
                    arg = 0
                    for k in range(len(fields)):
                        if PARAM_DICT[grade] == fields[k]:
                            arg = k
                    if platform[grade] == 0:
                        self.table.add_component(Label(), bg_color='Black', row=i + 3, column=arg)
                    else:
                        if names[i] == "סטיית תקן":
                            bg = bg_color_of_grade(platform[grade], platform="סטיית תקן", description="")
                        elif ARACHIM in grade:
                            bg = bg_color_of_grade(platform[grade], platform="", description=ARACHIM)
                        else:
                            bg = bg_color_of_grade(platform[grade], platform="", description="")
                        if math.floor(platform[grade]) == platform[grade]:
                            self.table.add_component(Label("{:.0f}".format(platform[grade]), fg_color='White'),
                                                     row=i + 3, column=arg, bg_color=bg)
                        else:
                            self.table.add_component(Label("{:.2f}".format(platform[grade]), fg_color='White'),
                                                     row=i + 3, column=arg, bg_color=bg)
        else:
            print(f"No grades for {self.selected_cadet}")
        self.gp.add_component(self.table, 3, 0)
        self.check_if_ready()

    """
    Generic functions, running when a certain input parameter has been inserted
    """

    def change_year(self, year):
        self.selected_year = year
        self.check_if_ready()

    def change_mode(self, up):
        self.update = up
        self.check_if_ready()

    def change_sem(self, sem):
        self.selected_sem = sem
        self.check_if_ready()

    def check_if_ready(self):
        if self.selected_sem and self.selected_year and self.selected_cadet and self.selected_mahzor:
            self.files_upload = UploadFiles(self.upload)
            self.gp.add_component(self.files_upload, 2, 0)
