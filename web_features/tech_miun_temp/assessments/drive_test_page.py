import os
import webbrowser
from dataclasses import fields

import web_framework.server_side.infastructure.constants as const
from web_features.tech_miun import permissions
from web_features.tech_miun.constants import SURVEY_NAME_DICT_KEY, MASTER_FILE_DICT_KEY, LINK_DICT_KEY, \
    HEBREW_NAME_DICT_KEY
from web_features.tech_miun.malshab_info import MalshabInfo, Malshab
from web_features.tech_miun.report_survey import ReportSurvey
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.hyper_link import HyperLink
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_framework.server_side.infastructure.page import Page

from web_framework.server_side.infastructure.page import Page
# standard Talpix page class to inherit from.
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_features.Elements.personal_page.modules.cadet_classes import *
from web_features.Elements.personal_page.permissions import *
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.constants import *
from web_features.tech_miun_temp.cadet_classes.utils import *
from web_features.tech_miun_temp.cadet_classes.miun_classess import CadetMiunGrades
import pandas as pd

SEMESTERS = ['סמסטר א', 'סמסטר ב', 'סמסטר ג', 'סמסטר ד', 'סמסטר ה', 'סמסטר ו']


class DriveTestPage(Page):

    def __init__(self, params):
        super().__init__(params)

    @staticmethod
    def get_title() -> str:
        return "drive test page"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_estimator_miun(user)

    def create_open_text_display(self, open_texts):
        sp = StackPanel([])
        for open_text in open_texts:
            sp.add_component(Label(open_text, fg_color='Black'))
            sp.add_component(Divider())
        return sp

    def get_page_ui(self, user: User):
        self.user = user
        self.sp = StackPanel([])

        # the relative path of the "interviews data" csv
        file_name = "test.xls"
        file_path = os.path.join(os.path.dirname(__file__), "../temp_files/"+file_name)

        # download the CSV data into ../cadet_classes
        drive_url = "https://drive.google.com/file/d/1azdCHg0AOO8d6bKhsQ-KvjyhXahvzkNV/view?usp=share_link"
        import_data_from_drive(drive_url, file_name)

        group_name = "Test"
        data_frame = CadetMiunGrades.load_data_from_csv_or_excel(file_path)
        group_data = [Data("Raw Data", data_frame)]

        # adding the grid panel with the interview data to talpix
        group_layout = GridPanel(2, len(group_data), bg_color=COLOR_PRIMARY_DARK)
        for index, data in enumerate(group_data):
            group_layout.add_component(Label(data.title, fg_color='White'), 0, index)
            if data.is_semesterial:
                semesters_layout = GridPanel(2, 6, bg_color='Green')
                for semester_num, semester in enumerate(SEMESTERS):
                    semesters_layout.add_component(Label(semester, fg_color='White'), 0, semester_num)
                    semesters_layout.add_component(Label(str(data.value[semester_num]), fg_color='White'), 1,
                                                   semester_num)
                group_layout.add_component(semesters_layout, 1, index)
            elif data.is_open:
                open_text_sp = StackPanel([])
                open_text_display = self.create_open_text_display(data.value)
                popup = PopUp(open_text_display, is_shown=False, is_cancelable=True, title=data.title)
                open_text_sp.add_component(Button(data.title, action=lambda p=popup: p.show()))
                open_text_sp.add_component(popup)
                group_layout.add_component(open_text_sp, 1, index)
            elif type(data.value) == pd.DataFrame:
                group_layout.add_component(data_frame_to_grid_panel(data.value))
            else:
                group_layout.add_component(Label(str(data.value), fg_color='White'), 1, index)

        example_accordion = Accordion([group_layout], [group_name])

        self.sp.add_component(example_accordion)
        print(data_frame.columns)
        # self.sp.add_component(Label(data_frame["candidate_name"], fg_color='Black'))
        self.sp.add_component(Label("", fg_color='Black'))

        return self.sp
