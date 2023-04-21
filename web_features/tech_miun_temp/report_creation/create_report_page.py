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
from web_features.tech_miun_temp.cadet_classes.utils import Data

SEMESTERS = ['סמסטר א','סמסטר ב','סמסטר ג','סמסטר ד','סמסטר ה','סמסטר ו']

class CreateReportPage(Page):

    def __init__(self, params):
        super().__init__(params)

    @staticmethod
    def get_title() -> str:
        return "יצירת דוח"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_estimator_miun(user)

    def on_id_selected(self, selection):
        print(selection)

    def on_path_selected(self, path):
        print(path)


    def get_page_ui(self, user: User):
        self.user = user
        self.sp = StackPanel([])
        ids = ["1","7"]
        id_combobox = ComboBox(ids, lambda selected: self.on_id_selected(ids[int(selected)]))
        self.sp.add_component(id_combobox)
        paths = ["kuku", "Damn"]
        path_combobox = ComboBox(paths, lambda selected: self.on_path_selected(paths[int(selected)]))
        self.sp.add_component(path_combobox)
        return self.sp

   