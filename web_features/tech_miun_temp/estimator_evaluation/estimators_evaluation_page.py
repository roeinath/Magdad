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
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.components.text_input import TextInput
from web_features.Elements.personal_page.permissions import *
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.constants import *
from web_features.tech_miun_temp.custom_components import FileChoosePopUpCreateReport
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.pop_up import PopUp
from APIs.ExternalAPIs.MiunDrive.MiunDriveAPI import get_list_of_all_data_files, open_file, FileTree, get_file_object, update_file
from APIs.TalpiotAPIs.User.user import User
from web_features.tech_miun_temp.wix.utils import ID_names
from web_features.tech_miun_temp.estimator_evaluation.evaluate_estimators import create_evaluators_report

from typing import *
import docx
import pandas as pd



class EstimatorsEvaluationPage(Page):

    def __init__(self, params):
        super().__init__(params)
        self.ti_input_path: TextInput = None  # TextInput with path to input template file for the report
        self.ti_output_path: TextInput = None  # TextInput with path to output destination

    @staticmethod
    def get_title() -> str:
        return "יצירת דוח מעריכים"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_estimator_miun(user)

    def get_page_ui(self, user: User):
        # Initialize user and StackPanel
        self.user = user
        self.sp = StackPanel([])

        # Label with title
        self.sp.add_component(Label("יצירת דוח למעריכים", size=SIZE_LARGE))

        # Input path TextInput
        self.ti_input_path = TextInput(text_holder="נתיב קובץ אקסל על המעריכים")
        self.sp.add_component(self.ti_input_path)

        # Output directory TextInput
        self.ti_output_path = TextInput(text_holder='נתיב הפלט')
        self.sp.add_component(self.ti_output_path)

        # Submit button
        btn_submit: Button = Button("עשה את הקסם!")
        btn_submit.set_action(
            action=lambda: create_evaluators_report(self.ti_input_path.text,
                                                                 self.ti_output_path.text))
        self.sp.add_component(btn_submit)

        return self.sp

