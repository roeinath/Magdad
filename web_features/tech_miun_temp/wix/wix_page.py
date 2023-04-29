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
from web_framework.server_side.infastructure.components.text_input import TextInput
from web_framework.server_side.infastructure.constants import *
from web_features.tech_miun_temp.cadet_classes.utils import Data
from web_features.tech_miun_temp.custom_components import FileChoosePopUp
from APIs.ExternalAPIs.MiunDrive.MiunDriveAPI import get_list_of_all_data_files, update_file, open_file



class WixPage(Page):

    def __init__(self, params):
        super().__init__(params)

    @staticmethod
    def get_title() -> str:
        return "Wix מיון"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_estimator_miun(user)

    def create_group(self):
        sp = StackPanel([])
        label1 = Label("טקסט 1")
        label2 = Label("טקסט 2")
        example_gridpanel = GridPanel(1, 2, bg_color=COLOR_PRIMARY_LIGHT, bordered=True)
        example_gridpanel.add_component(label1, 0, 0)
        example_gridpanel.add_component(label2, 0, 1)
        sp.add_component(example_gridpanel)
        self.group_num += 1
        pass

    def get_page_ui(self, user: User):
        self.user = user
        self.sp = StackPanel([])
        
        popup = FileChoosePopUp(on_file_chosen=lambda f: print(f), is_shown=False, is_cancelable=True, title="כותרת")
        button = Button("בחר\י קובץ", action=lambda p=popup: p.show())

        ti = TextInput(text_holder='gg')

        self.sp.add_component(popup)
        self.sp.add_component(button)
        self.sp.add_component(ti)
        self.sp.add_component(Button("צור קבוצה", action=lambda: print(ti.text)))

        self.group_num = 0
        button = Button("צור קבוצה", action=lambda: self.create_group())
        
        return self.sp

   