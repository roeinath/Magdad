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
from web_features.Elements.personal_page.modules.cadet_classes import *
from web_features.Elements.personal_page.permissions import *
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.constants import *
from web_features.tech_miun_temp.cadet_classes.utils import Data
from web_features.tech_miun_temp.custom_components import FileChoosePopUpCreateReport
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.pop_up import PopUp
from APIs.ExternalAPIs.MiunDrive.MiunDriveAPI import get_list_of_all_data_files, open_file, FileTree, get_file_object, update_file
from APIs.TalpiotAPIs.User.user import User
from web_features.tech_miun_temp.wix.utils import ID_NAMES

from typing import *
import docx
import pandas as pd


class CreateReportPage(Page):

    def __init__(self, params):
        super().__init__(params)
        self.ti_wanted_values: List[TextInput] = []  # List of all TextInputs in the grid
        self.files: List[FileTree] = []  # List of all file paths chosen by user
        self.fields: List[str] = []  # List of all fields chosen by user
        self.rows_created: int = 0  # Number of rows created in the grid

    @staticmethod
    def get_title() -> str:
        return "חיפוש קבוצה"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_estimator_miun(user)

    def on_id_selected(self, selection):
        print(selection)

    def on_path_selected(self, path):
        print(path)

    def get_page_ui(self, user: User):
        # Initialize user and StackPanel
        self.user = user
        self.sp = StackPanel([])

        # Horizontal StackPanel
        grid = GridPanel(100, 3, bordered=True)
        self.sp.add_component(grid)
        self.add_row(grid)

        # Add rows Button
        btn_add_row: Button = Button("הוסף שורה")
        btn_add_row.set_action(action=lambda: self.add_row(grid))
        self.sp.add_component(btn_add_row)

        # Submit button
        btn_submit: Button = Button("עשה את הקסם!")
        btn_submit.set_action(
            action=lambda: print(self.generate_key_value_dictionary()))
        self.sp.add_component(btn_submit)

        return self.sp

    def add_row(self, grid: GridPanel) -> None:
        num_row: int = self.rows_created

        # Key TextInput
        ti_key: TextInput = TextInput(text_holder='מה הערך צריך להיות')
        self.ti_wanted_values.append(ti_key)

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

    def generate_group_ids_list(self) -> List[str]:
        """
        Use data accumulated in pages attributes to generate a dictionary that matches each key
        to the value it needs to be replaces by.
        """

        group_ids_list: List[str] = ['']

        for i in range(len(self.ti_wanted_values)):
            # Get key for the dictionary
            wanted_value: str = self.ti_wanted_values[i].text

            # Get file in df format
            file: FileTree = self.files[i]
            update_file(file)
            df: pd.DataFrame = open_file(file)

            id_field_name: str = ''
            # Get field name of id 
            for field in ID_NAMES:
                if field not in df:
                    continue
                id_field_name: str = field
            if not id_field_name:
                raise Exception("ID Field Not Found")

            # Get specific value from df
            field_name: str = self.fields[i]

            # Get all the rows that the field equals the wanted value
            group_candidates_ids_row: df = df[df[field_name].astype(str) == wanted_value][id_field_name]

            # Add pair to the dictionary
            if not group_ids_list[0]:
                group_ids_list = list(group_candidates_ids_row)
            else:
                # Calculate intersection of lists of candidates
                group_ids_list = [val for val in group_ids_list if val in list(group_candidates_ids_row)] 

        return group_ids_list

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
        field_list: List[str] = CreateReportPage.get_field_list(file)
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

