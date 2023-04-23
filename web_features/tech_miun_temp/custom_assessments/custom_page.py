import webbrowser
from dataclasses import fields
import json
import os

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
from web_features.tech_miun_temp.cadet_classes.utils import Data
from APIs.ExternalAPIs.MiunDrive.MiunDriveAPI import get_list_of_all_data_files, update_file
from web_features.tech_miun_temp.custom_assessments.utils import fetch_fields_dict


class CustomPage(Page):

    def __init__(self, params):
        super().__init__(params)

    @staticmethod
    def get_title() -> str:
        return "עיצוב חופשי"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_estimator_miun(user)

    def get_page_ui(self, user: User):
        self.user = user
        self.sp = StackPanel([])
        
        with open(os.path.join(os.path.abspath(__file__), '..','custom.json'),'r') as f:
            groups_dict = json.load(f)
            root = get_list_of_all_data_files()
            #print('Now\n',fetch_fields_dict(root, groups_dict, 12),'\nEND')
            group_names = []
            group_layouts = []
            for group_name, fields_list in groups_dict.items():
                group_names.append(group_name)
                group_layout = GridPanel(2, len(fields_list), bg_color=COLOR_PRIMARY_DARK)
                for index, field in enumerate(fields_list):
                    group_layout.add_component(Label(field, fg_color='White'), 0, index)
                    group_layout.add_component(Label("GG", fg_color='White'), 1, index)
                group_layouts.append(group_layout)

            accordion = Accordion(group_layouts, group_names)
            self.sp.add_component(accordion)

        return self.sp

   