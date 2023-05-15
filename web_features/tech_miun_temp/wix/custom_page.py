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
from APIs.ExternalAPIs.MiunDrive.MiunDriveAPI import get_list_of_all_data_files, update_file, open_file, get_file_object
from web_features.tech_miun_temp.wix.utils import fetch_fields_dict, ID_names, CUSTOM_PAGES_DIR


class CustomPage(Page):
    person_id = 0

    def __init__(self, params):
        super().__init__(params)

    @staticmethod
    def get_title() -> str:
        return "עיצוב חופשי"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_estimator_miun(user)

    def fetch_field_values(self, user, root, person_id, field):
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print(self.person_id)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        name_file = field.split(':')[0]
        name_column = field.split(':')[1]
        self.user = user
        self.file_combos = []
        self.current_file = root
        self.files = [root]
        print('##################################')
        children = root.get_all_children()
        self.current_file = get_file_object(root, name_file)
        print('##################################')
        update_file(self.current_file)
        self.df = open_file(self.current_file)  # opens file as pandas dataframe
        for id_name in ID_names:
            if (id_name in self.df):
                print(self.df[self.df[id_name] == person_id])
                value = self.df.loc[self.df[id_name] == person_id, name_column].iloc[0]
                print('##################################')
                print(value)
                return value
        raise Exception('No ID Field')

    def return_id(self, number, user):
        self.person_id = int(number)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print(self.person_id)
        print(number)
        self.update_page(user)

    def update_page(self, user):
        with open(os.path.join(CUSTOM_PAGES_DIR, self.selected_page_name), 'r') as f:
            groups_dict = json.load(f)
            root = get_list_of_all_data_files()
            group_names = []
            for group_name, fields_list in groups_dict.items():
                group_names.append(group_name)
                for index, field in enumerate(fields_list):
                    real_value = self.fetch_field_values(user, root, self.person_id, field)
                    self.labels[field].update_text(real_value)

    def update_custom_page_opened(self, page_name):
        self.custom_stack.clear()
        self.selected_page_name = page_name
        # self.cadet_id=self.get_id(user)

        id_utils = [str(u.click_email).split('@')[0] for u in User.objects()]
        name_utils = [str(u.name) for u in User.objects()]
        self.custom_stack.add_component(
            ComboBox(name_utils, on_changed=lambda person_id: self.return_id(id_utils[int(person_id)], self.user)),
            index=0)

        # fetch_fields_dict(root: FileTree, json_dict: dict, candidate_id: int)
        with open(os.path.join(CUSTOM_PAGES_DIR, page_name), 'r') as f:
            groups_dict = json.load(f)
            root = get_list_of_all_data_files()
            # print('Now\n',fetch_fields_dict(root, groups_dict, 12),'\nEND')
            group_names = []
            group_layouts = []
            self.labels = {}
            for group_name, fields_dict in groups_dict.items():
                group_names.append(group_name)
                group_layout = GridPanel(2, len(list(fields_dict.values())), bg_color=COLOR_PRIMARY_DARK)
                index = 0
                for field_name, field in fields_dict.items():
                    group_layout.add_component(Label(field_name, fg_color='White'), 0, index)
                    real_value = self.fetch_field_values(self.user, root, self.person_id, field)
                    self.labels[field] = Label(real_value, fg_color='White')
                    print('##########################')
                    group_layout.add_component(self.labels[field], 1, index)  # real_value_dict[field]
                    index += 1
                group_layouts.append(group_layout)

            accordion = Accordion(group_layouts, group_names)
            self.custom_stack.add_component(accordion)
            # self.sp.add_component(self.custom_stack)

    def get_page_ui(self, user: User):
        self.user = user
        self.sp = StackPanel([])
        self.custom_stack = StackPanel([])

        custom_pages_files = []
        for file in os.listdir(CUSTOM_PAGES_DIR):
            if file.endswith('.json'):
                custom_pages_files.append(file)

        self.sp.add_component(
            ComboBox(custom_pages_files,
                     on_changed=lambda chosen_ind: self.update_custom_page_opened(custom_pages_files[int(chosen_ind)]))
        )

        self.sp.add_component(self.custom_stack)

        return self.sp

