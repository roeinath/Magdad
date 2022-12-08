from dataclasses import fields

import web_framework.server_side.infastructure.constants as const
from web_features.tech_miun.status_manager import StatusManager
from web_framework.server_side.infastructure.components.button import Button
from web_features.tech_miun.report_survey import ReportSurvey
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
import webbrowser
import web_features.tech_miun.constants as miun_const
from web_framework.server_side.infastructure.components.hyper_link import HyperLink

from web_features.tech_miun import permissions
from web_features.tech_miun.malshab_info import MalshabInfo, Malshab


# TODO: add documentation to class and methods
LINK = "link"
SURVEY_NAME = "survey_name"


class Web:

    def __init__(self, link):
        self._link = link

    def __call__(self):
        webbrowser.open_new_tab(self._link)


class EstimatorPage(Page):

    def __init__(self, params):
        super().__init__()
        self.sp = None
        self._malshab_table = []
        self._malshab_info = {}
        self.refresh_filed()
        self._report_survey = ReportSurvey()

    def refresh_filed(self):
        self._malshab_info = {"SOLUTIONS": MalshabInfo(miun_const.SOLUTIONS),
                              "HACKAB": MalshabInfo(miun_const.HACKAB),
                              "QA": MalshabInfo(miun_const.QA)}

    @staticmethod
    def get_title() -> str:
        return "דף מעריך"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_estimator_miun(user)

    def add_value(self, val, table_number, row, col):
        # todo: rename method to be more self explanatory
        if type(val) == str:
            self._malshab_table[table_number].add_component(Label(text=val, size=const.SIZE_MEDIUM), row, col)
        elif type(val) == int:
            self._malshab_table[table_number].add_component(Label(text=str(val), size=const.SIZE_MEDIUM), row, col)
        else:
            if val:
                self._malshab_table[table_number].add_component(
                    Label(text="", size=const.SIZE_MEDIUM, fg_color=const.COLOR_PRIMARY_LIGHT,
                          bg_color=const.COLOR_TRANSPARENT), row, col)
            else:
                self._malshab_table[table_number].add_component(
                    Label(text="Need to fill survey", size=const.SIZE_MEDIUM,
                          fg_color=const.COLOR_PRIMARY_LIGHT,
                          bg_color=const.COLOR_PRIMARY_DARK), row, col)

    def add_malshab(self, table_number, malshab, row_number):
        for i, field in enumerate(fields(malshab)):
            self.add_value(getattr(malshab, field.name), table_number, row_number, i + 1)

    def add_survey_for_malshab(self, table_number, row_number, survey):
        button = HyperLink(survey[SURVEY_NAME], bold=True, url=survey[LINK])

        self._malshab_table[table_number].add_component(button, row_number, 0)

    def get_page_ui(self, user):
        self.sp = StackPanel([])
        title = Label(text="מילוי הערכות\n מעריך: " + user.name, size=const.SIZE_EXTRA_LARGE,
                      fg_color=const.COLOR_PRIMARY_DARK, bold=True)
        self.sp.add_component(title)
        survey_list = self._report_survey.get_surveys()
        for i, survey in enumerate(survey_list):
            self.sp.add_component(Label(text=survey[SURVEY_NAME], size=const.SIZE_LARGE))
            self.add_survey_table(user, i, self._malshab_info[survey[SURVEY_NAME]].get_malshabs_by_estimator(user),
                                  survey)

        return self.sp

    def add_survey_table(self, estimator, table_number, malshab_list, survey):
        self._malshab_table.append(GridPanel(len(malshab_list) + 1, len(fields(Malshab)) +
                                             2, bg_color=const.COLOR_TRANSPARENT))

        set_title_table(self._malshab_table[table_number])
        for malshab_index in range(len(malshab_list)):
            self.add_survey_for_malshab(table_number, malshab_index + 1,
                                        self._report_survey.generate_survey(survey, estimator,
                                                                            malshab_list[malshab_index]))
            self.add_malshab(table_number, malshab_list[malshab_index], malshab_index + 1)

        self.sp.add_component(self._malshab_table[table_number])


def set_title_table(table):
    table.add_component(Label("הערכות למילוי", bold=True, size=const.SIZE_MEDIUM, fg_color='white'), 0, 0,
                            bg_color=const.COLOR_PRIMARY_DARK)
    data = ["שם פרטי", "מספר סידורי", "כיתה", "צוות"]

    for i in range(len(data)):
        table.add_component(Label(text=data[i], bold=True, size=const.SIZE_MEDIUM, fg_color='white'), 0, i + 1,
                            bg_color=const.COLOR_PRIMARY_DARK)
