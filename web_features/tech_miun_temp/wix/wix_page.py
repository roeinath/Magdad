import webbrowser
from dataclasses import fields
import json
import os
from os import path
from typing import *

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
from web_features.tech_miun_temp.custom_components import FileChoosePopUpCreateReport
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from APIs.ExternalAPIs.MiunDrive.MiunDriveAPI import get_list_of_all_data_files, open_file, FileTree, get_file_object, FileTree, update_file

CUSTOM_PAGES_DIR = os.path.join(path.abspath(__file__), '..', 'custom_pages')

class WixPage(Page):

    def __init__(self, params):
        super().__init__(params)
        self.ti_keys: List[TextInput] = []  # List of all TextInputs in the grid
        self.files: List[FileTree] = []  # List of all file paths chosen by user
        self.fields: List[str] = []  # List of all fields chosen by user
        self.rows_created: int = 0  # Number of rows created in the grid
        self.ti_page_name: TextInput = None  # TextInput with path to output destination

    @staticmethod
    def get_title() -> str:
        return "Wix מיון"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_estimator_miun(user)

    def get_page_ui(self, user: User):
        # Initialize user and StackPanel
        self.user = user
        self.sp = StackPanel([])

        # Cadet id TextInput
        self.ti_page_name = TextInput(text_holder='הגדר שם לעמוד')
        self.sp.add_component(self.ti_page_name)

        # Horizontal StackPanel
        grid = GridPanel(100, 3, bordered=True)
        self.sp.add_component(grid)
        self.add_row(grid)

        # Add rows Button
        btn_add_row: Button = Button("הוסף שורה")
        btn_add_row.set_action(action=lambda: self.add_row(grid))
        self.sp.add_component(btn_add_row)
        # Submit button
        btn_submit: Button = Button("צור עמוד")
        btn_submit.set_action(
            action=lambda: self.create_json_for_page(self.ti_page_name.text, self.generate_name_value_dictionary()))
        self.sp.add_component(btn_submit)

        return self.sp

    def add_row(self, grid: GridPanel) -> None:
        num_row: int = self.rows_created

        # Key TextInput
        ti_key: TextInput = TextInput(text_holder="שם הנתון")
        self.ti_keys.append(ti_key)

        # File Button
        btn_file: Button = Button("בחר קובץ")
        btn_file.set_action(action=lambda: self.open_file_choice_form(num_row, grid))
        self.files.append(None)

        # Field Combobox
        self.fields.append("")

        # Add to grid
        grid.add_component(ti_key, num_row, 0)
        grid.add_component(btn_file, num_row, 1)

        self.rows_created += 1

    def generate_name_value_dictionary(self) -> Dict[str, str]:
        """
        Use data accumulated in pages attributes to generate a dictionary that matches each key
        to the value it needs to be replaces by.
        """
        key_value_dict: Dict[str, str] = {}

        for i in range(len(self.ti_keys)):
            # Get key for the dictionary
            key: str = self.ti_keys[i].text

            # Get full path of file
            if self.files[i]:
                file_path: str = self.files[i].get_full_path()[1:]
                field_name: str = self.fields[i]

                #Value is in format of file_path:field_name
                value: str = f'{file_path}:{field_name}'

                # Add pair to the dictionary
                key_value_dict[key] = value
        return key_value_dict

    def open_file_choice_form(self, num_row: int, grid: GridPanel) -> None:
        """
        Opens a popup in which user chooses a certain file from the MuinDrive file tree.
        @param num_row: The number of row that called the function.
                        Used to enter the file path into the array in the proper location.
        @param grid: Grid to add pass on to handle_file_chosen
        """
        popup = FileChoosePopUpCreateReport(
            on_file_chosen=lambda file: self.handle_file_chosen(file, num_row, grid),
            is_shown=False,
            is_cancelable=True,
            title="בחר/י קובץ")
        self.sp.add_component(popup)
        popup.show()

    def handle_file_chosen(self, file: FileTree, num_row: int, grid: GridPanel) -> None:
        # Insert file path into list
        self.files[num_row] = file

        # Open fields combobox
        field_list: List[str] = WixPage.get_field_list(file)
        cb_field: ComboBox = ComboBox(field_list,
                                      on_changed=lambda ind: self.update_list_fields(field_list[int(ind)], num_row))

        grid.add_component(cb_field, num_row, 2)

        # Replace choose file button with file chosen label
        # file_path: str = file.get_full_path()
        label_file_chosen: Label = Label(file.title)
        grid.add_component(label_file_chosen, num_row, 1)

    def update_list_fields(self, new_val: str, ind: int) -> None:
        self.fields[ind] = new_val

    @staticmethod
    def get_field_list(file: FileTree) -> List[str]:
        """
        Returns a list of strings of all fields in a specific file
        """
        update_file(file)
        df: pd.DataFrame = open_file(file)
        fields = [str(i) for i in df]
        return fields

    def create_json_for_page(self, page_name:str, key_value_dict: Dict[str, str]):
        # Creates PageName.json file inside CUSTOM_PAGE_DIR
        new_dict = {'roei':key_value_dict}
        new_page_json_path: str = os.path.join(CUSTOM_PAGES_DIR, page_name)
        with open(f"{new_page_json_path}.json", "w+") as outfile:
            json.dump(new_dict, outfile)

   