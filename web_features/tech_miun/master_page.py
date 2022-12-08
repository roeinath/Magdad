from dataclasses import fields

import web_framework.server_side.infastructure.constants as const
from web_features.tech_miun import permissions
from web_features.tech_miun.drive_connection import DriveConnection
from web_features.tech_miun.status_manager import StatusManager
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_framework.server_side.infastructure.components.button import Button
from web_features.tech_miun.report_survey import ReportSurvey
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.hyper_link import HyperLink
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
import web_features.tech_miun.constants as miun_const

from web_features.tech_miun.malshab_info import MalshabInfo

SURVEY_NAME = "survey_name"
NUMBER_OF_MALSHABS_PER_ESTIMATOR = 5
DATA = ["מעריך"] + ['מלש"ב/ית'] * NUMBER_OF_MALSHABS_PER_ESTIMATOR


class MasterPage(Page):

    def __init__(self, params):
        super().__init__()
        self.sp = None
        self._status_table = []
        self._malshab_info = {}
        self._status_managers = {}
        self.refresh_filed()
        self._report_survey = ReportSurvey()

        try:
            self.drive_connection = DriveConnection()
        except FileNotFoundError:
            self.drive_connection = None

    def refresh_filed(self):
        self._malshab_info = {"SOLUTIONS": MalshabInfo(miun_const.SOLUTIONS),
                              "HACKAB": MalshabInfo(miun_const.HACKAB),
                              "QA": MalshabInfo(miun_const.QA)}
        self._status_managers = {"SOLUTIONS": StatusManager(miun_const.SOLUTION_RESULTS),
                                 "HACKAB": StatusManager(miun_const.HACKAB_RESULTS),
                                 "QA": StatusManager(miun_const.QA_RESULTS)}

    @staticmethod
    def get_title() -> str:
        return "מצב הערכות כללי"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_master_miun(user)

    def add_malshab_status(self, survey, estimator_email, malshab, table_number, row, col):
        text = f"{malshab.name} ({malshab.serial_number})"

        if self._status_managers[survey[SURVEY_NAME]].is_filled(estimator_email, malshab):
            text += " - ✅"
        else:
            text += " - ❌"

        malshab_label = Label(text, size=const.SIZE_MEDIUM, fg_color=const.COLOR_BLACK)
        self._status_table[table_number].add_component(malshab_label, row, col)

    def add_estimator(self, survey, table_number, estimator_email, row):
        estimator_name = self._malshab_info[survey[SURVEY_NAME]].get_estimator_name_by_email(estimator_email)
        estimator_label = Label(estimator_name, size=const.SIZE_MEDIUM, fg_color=const.COLOR_BLACK)
        self._status_table[table_number].add_component(estimator_label, row, 0)

        malshabs = self._malshab_info[survey[SURVEY_NAME]].get_malshabs_by_estimator_email(estimator_email)
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
        self.sp.add_component(HyperLink('מאסטר solution', bold=True, url=miun_const.SOLUTIONS_MASTER_URL))
        self.sp.add_component(HyperLink('מאסטר חק"ב', bold=True, url=miun_const.HACKAB_MASTER_URL))
        self.sp.add_component(HyperLink('מאסטר QA', bold=True, url=miun_const.QA_MASTER_URL))
        refresh_button = Button(" ♻️ " + "רענון נתונים ", self.update_data_from_drive, bg_color=const.COLOR_GREEN)
        self.sp.add_component(refresh_button)
        survey_list = self._report_survey.get_surveys()
        survey_titles = []
        survey_tables = []
        for i, survey in enumerate(survey_list):
            estimator_email_list = self._malshab_info[survey[SURVEY_NAME]].get_all_estimator()
            table = self.survey_table(i, estimator_email_list, survey)
            survey_titles.append(survey[SURVEY_NAME])
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
        title = Label(text="מילוי הערכות טבלת מצב: " + survey[SURVEY_NAME], size=const.SIZE_LARGE,
                      fg_color=const.COLOR_PRIMARY_DARK, bold=True)
        survey_table_sp.add_component(title)

        self._status_table.append(GridPanel(len(estimator_email_list) + 1, len(DATA), bg_color=const.COLOR_TRANSPARENT))

        set_title_table(self._status_table[table_number], survey)
        for estimator_index in range(len(estimator_email_list)):
            self.add_estimator(survey, table_number, estimator_email_list[estimator_index], estimator_index + 1)

        survey_table_sp.add_component(self._status_table[table_number])
        return survey_table_sp


def set_title_table(table, survey):
    for i in range(len(DATA)):
        table.add_component(Label(text=DATA[i], bold=True, size=const.SIZE_MEDIUM, fg_color='white'), 0, i,
                            bg_color=const.COLOR_PRIMARY_DARK)
