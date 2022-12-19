import web_framework.server_side.infastructure.constants as const
from web_features.tech_miun import permissions
from web_features.tech_miun.constants import SURVEY_NAME_DICT_KEY, MASTER_FILE_DICT_KEY, SURVEY_LIST_ALL, \
    RESULT_FILE_DICT_KEY, MASTER_URL_DICT_KEY, HEBREW_NAME_DICT_KEY
from web_features.tech_miun.drive_connection import DriveConnection
from web_features.tech_miun.malshab_info import MalshabInfo
from web_features.tech_miun.report_survey import ReportSurvey
from web_features.tech_miun.status_manager import StatusManager
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.hyper_link import HyperLink
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.page import Page

MAX_MALSHABS_PER_ESTIMATOR = 10
MIN_MALSHABS_PER_ESTIMATOR = 5
DATA = ["מעריך"] + ['מלש"ב/ית'] * MAX_MALSHABS_PER_ESTIMATOR


class MasterPage(Page):

    def __init__(self, params):
        super().__init__()
        self.sp = None
        self._status_table = []
        self._malshab_info = {}
        self._status_managers = {}
        self._survey_list = SURVEY_LIST_ALL
        for survey in self._survey_list:
            self._malshab_info[survey[SURVEY_NAME_DICT_KEY]] = MalshabInfo(survey[MASTER_FILE_DICT_KEY])
            self._status_managers[survey[SURVEY_NAME_DICT_KEY]] = StatusManager(survey[RESULT_FILE_DICT_KEY])

        self._report_survey = ReportSurvey()

        try:
            self.drive_connection = DriveConnection()
        except FileNotFoundError:
            self.drive_connection = None

    def refresh_filed(self):
        for sur in self._survey_list:
            self._malshab_info[sur[SURVEY_NAME_DICT_KEY]].load_local_file()
            self._status_managers[sur[SURVEY_NAME_DICT_KEY]].load_local_file()

    @staticmethod
    def get_title() -> str:
        return "מצב הערכות כללי"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_master_miun(user)

    def add_malshab_status(self, survey, estimator_email, malshab, table_number, row, col):
        text = f"{malshab.name} ({malshab.serial_number})"

        if self._status_managers[survey[SURVEY_NAME_DICT_KEY]].is_filled(estimator_email, malshab):
            text += " - ✅"
        else:
            text += " - ❌"

        malshab_label = Label(text, size=const.SIZE_MEDIUM, fg_color=const.COLOR_BLACK)
        self._status_table[table_number].add_component(malshab_label, row, col)

    def add_estimator(self, survey, table_number, estimator_email, row):
        estimator_name = self._malshab_info[survey[SURVEY_NAME_DICT_KEY]].get_estimator_name_by_email(estimator_email)
        estimator_label = Label(estimator_name, size=const.SIZE_MEDIUM, fg_color=const.COLOR_BLACK)
        self._status_table[table_number].add_component(estimator_label, row, 0)

        malshabs = self._malshab_info[survey[SURVEY_NAME_DICT_KEY]].get_malshabs_by_estimator_email(estimator_email)
        for malshab_index, malshab in enumerate(malshabs):
            self.add_malshab_status(survey, estimator_email, malshab, table_number, row, malshab_index + 1)

    def get_page_ui(self, user):
        self.sp = StackPanel([])
        self.draw()
        return self.sp

    def draw(self):
        self.sp.clear()
        if self.drive_connection is None:
            self.sp.add_component(
                Label(text="לא נמצא מפתח הצפנה למשיכה", size=const.SIZE_LARGE, fg_color='red', bold=True))
            return self.sp
        title = Label(text="מילוי הערכות טבלת מצב\n", size=const.SIZE_EXTRA_LARGE,
                      fg_color=const.COLOR_PRIMARY_DARK, bold=True)
        self.sp.add_component(title)
        master_prefix = 'מאסטר '
        refresh_button = Button(" ♻️ " + "רענון נתונים ", self.update_data_from_drive, bg_color=const.COLOR_GREEN)
        self.sp.add_component(refresh_button)
        horizonal_sp_links = StackPanel([], orientation=const.HORIZONTAL)
        for survey in self._survey_list[:-1]:
            horizonal_sp_links.add_component(
                HyperLink(master_prefix + survey[HEBREW_NAME_DICT_KEY], bold=True, url=survey[MASTER_URL_DICT_KEY]))
            space = chr(160) * 3  # just a little hack to add a space, normal space is not working
            horizonal_sp_links.add_component(Label(space + "|" + space))
        horizonal_sp_links.add_component(
            HyperLink(master_prefix + self._survey_list[-1][HEBREW_NAME_DICT_KEY], bold=True,
                      url=self._survey_list[-1][MASTER_URL_DICT_KEY]))
        self.sp.add_component(horizonal_sp_links)
        survey_titles = []
        master_links = []
        survey_tables = []
        for i, survey in enumerate(self._survey_list):
            estimator_email_list = self._malshab_info[survey[SURVEY_NAME_DICT_KEY]].get_all_estimator()
            table = self.survey_table(i, estimator_email_list, survey)
            survey_titles.append(survey[HEBREW_NAME_DICT_KEY])
            survey_tables.append(table)

        self.sp.add_component(Accordion(survey_tables, survey_titles))

    def update_data_from_drive(self):
        self.drive_connection()
        self.refresh_filed()
        self._status_table = []
        self.sp.clear()
        self.draw()

    def survey_table(self, table_number, estimator_email_list, survey):
        survey_table_sp = StackPanel([])
        title = Label(text="מילוי הערכות טבלת מצב: " + survey[HEBREW_NAME_DICT_KEY], size=const.SIZE_LARGE,
                      fg_color=const.COLOR_PRIMARY_DARK, bold=True)
        survey_table_sp.add_component(title)

        max_malshabs_of_estimator = self._malshab_info[survey[SURVEY_NAME_DICT_KEY]].get_max_malshabs_of_estimator()
        malshab_columns = max(MIN_MALSHABS_PER_ESTIMATOR, min(MAX_MALSHABS_PER_ESTIMATOR, max_malshabs_of_estimator))

        self._status_table.append(GridPanel(len(estimator_email_list) + 1, 1 + malshab_columns, bg_color=const.COLOR_TRANSPARENT))

        set_title_table(self._status_table[table_number], survey, malshab_columns)
        for estimator_index in range(len(estimator_email_list)):
            self.add_estimator(survey, table_number, estimator_email_list[estimator_index], estimator_index + 1)

        survey_table_sp.add_component(self._status_table[table_number])
        return survey_table_sp


def set_title_table(table, survey, malshab_columns):
    for i in range(1 + malshab_columns):
        table.add_component(Label(text=DATA[i], bold=True, size=const.SIZE_MEDIUM, fg_color='white'), 0, i,
                            bg_color=const.COLOR_PRIMARY_DARK)
