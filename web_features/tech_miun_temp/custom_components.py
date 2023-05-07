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
from APIs.ExternalAPIs.MiunDrive.MiunDriveAPI import get_list_of_all_data_files, update_file, open_file

class FileChoosePopUp(PopUp):
    def __init__(self, on_file_chosen, *params, **kargs):
        sp = self.initialize()
        self.on_file_chosen = on_file_chosen
        super().__init__(sp, *params, **kargs)

    def on_select_combo_box(self, selected_file):
        self.current_file = self.current_file.get_child(selected_file)
        children = self.current_file.get_all_children()
        if(children):
            self.file_combos.append(ComboBox(children,
                                            on_changed=lambda selected_file: self.on_select_combo_box(children[int(selected_file)])))
            self.sp.add_component(self.file_combos[-1])
        else:
            print("found file")
            button = Button("בחר\י קובץ", action=lambda: self.on_file_chosen(self.current_file))
            self.sp.add_component(button)

    def initialize(self):
        self.sp = StackPanel([])
        self.file_combos = []

        root = get_list_of_all_data_files()
        self.current_file = root
        children = root.get_all_children()
        if(children):
            self.file_combos.append(ComboBox(children,
                                        on_changed=lambda selected_file: self.on_select_combo_box(children[int(selected_file)])))
        else:
            #print an error
            pass

        self.sp.add_component(self.file_combos[0])
        
        return self.sp

