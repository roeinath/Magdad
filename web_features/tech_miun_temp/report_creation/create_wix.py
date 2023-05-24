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
from web_features.tech_miun_temp.custom_components import DataChoosePopUp
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.pop_up import PopUp
from APIs.ExternalAPIs.MiunDrive.MiunDriveAPI import get_list_of_all_data_files, open_file, FileTree, get_file_object, update_file
from APIs.TalpiotAPIs.User.user import User

from typing import *
import docx
import pandas as pd

ID_NAMES = ['id', 'ID', 'תעודת זהות', 'מספר זהות']

StatisticFunction = Callable[[List[pd.DataFrame], str], Any]
GraphFunction = Callable[[List[float]], None]
FunctionsDict = Dict[str, GraphFunction]

class CreateWixPage(Page):

    def __init__(self, params):
        super().__init__(params)
        self.ti_input_path: TextInput = None  # TextInput with path to input template file for the report
        self.ti_cadet_id: TextInput = None  # TextInput with the cadet id
        self.ti_keys: List[TextInput] = []  # List of all TextInputs in the grid
        self.json_strings: List[str] = [] # List of json strings generated
        self.files: List[FileTree] = []  # List of all file paths chosen by user
        self.fields: List[str] = []  # List of all fields chosen by user
        self.rows_created: int = 0  # Number of rows created in the grid
        self.ti_output_path: TextInput = None  # TextInput with path to output destination

    @staticmethod
    def get_title() -> str:
        return "יצירת וויקס"

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

        # Input path TextInput
        self.ti_input_path = TextInput(text_holder='נתיב קובץ תבנית הדו"ח')
        self.sp.add_component(self.ti_input_path)

        # Cadet id TextInput
        self.ti_cadet_id = TextInput(text_holder='ת"ז של הצוער')
        self.sp.add_component(self.ti_cadet_id)

        # Horizontal StackPanel
        grid = GridPanel(100, 2, bordered=True)
        self.sp.add_component(grid)
        self.add_row(grid)

        # Add rows Button
        btn_add_row: Button = Button("הוסף שורה")
        btn_add_row.set_action(action=lambda: self.add_row(grid))
        self.sp.add_component(btn_add_row)

        # Output directory TextInput
        self.ti_output_path = TextInput(text_holder='נתיב הפלט')
        self.sp.add_component(self.ti_output_path)

        # Submit button
        btn_submit: Button = Button("עשה את הקסם!")
        btn_submit.set_action(
            action=lambda: CreateWixPage.create_single_report(self.ti_input_path.text,
                                                                 self.ti_output_path.text,
                                                                 self.generate_key_value_dictionary()))
        self.sp.add_component(btn_submit)

        return self.sp

    def add_row(self, grid: GridPanel) -> None:
        num_row: int = self.rows_created

        # Key TextInput
        ti_key: TextInput = TextInput(text_holder='שם קוד')
        self.ti_keys.append(ti_key)

        # File Button
        btn_file: Button = Button("בחר/י הצגה")
        btn_file.set_action(action=lambda: self.open_data_choice_form(num_row, grid))
        self.files.append(None)

        # Field Combobox
        self.fields.append("")

        # Add to grid
        grid.add_component(ti_key, num_row, 0)
        grid.add_component(btn_file, num_row, 1)

        self.rows_created += 1

    def generate_key_value_dictionary(self) -> Dict[str, str]:
        """
        Use data accumulated in pages attributes to generate a dictionary that matches each key
        to the value it needs to be replaces by.
        """
        key_value_dict: Dict[str, str] = {}

        for i in range(len(self.ti_keys)):
            # Get key for the dictionary
            key: str = self.ti_keys[i].text

            # Get file in df format
            file: FileTree = self.files[i]
            update_file(file)
            df: pd.DataFrame = open_file(file)

            # Get specific value from df
            field_name: str = self.fields[i]
            cadet_id: str = self.ti_cadet_id.text
            # Retrieve the cell value based on the column name and row value
            value: str = "אין ערך תקין"
            for field in ID_NAMES:
                if field not in df:
                    continue
                row = df[df[field].astype(int).astype(str) == cadet_id]
                if len(row) > 0:
                    value = str(row[field_name].iloc[0])

            # Add pair to the dictionary
            key_value_dict[key] = value
        return key_value_dict

    def open_data_choice_form(self, num_row: int, grid: GridPanel) -> None:
        """
        Opens a popup in which user chooses a certain file from the MuinDrive file tree.
        @param num_row: The number of row that called the function.
                        Used to enter the file path into the array in the proper location.
        @param grid: Grid to add pass on to handle_file_chosen
        """
        popup = DataChoosePopUp(
            on_file_chosen=lambda file: self.handle_file_chosen(file, num_row, grid),
            is_shown=False,
            is_cancelable=True,
            title="בחר/י הצגת נתונים")
        self.sp.add_component(popup)
        popup.show()

    def handle_file_chosen(self, file: FileTree, num_row: int, grid: GridPanel) -> None:
        # Insert file path into list
        self.files[num_row] = file

        # Open fields combobox
        field_list: List[str] = CreateWixPage.get_field_list(file)
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
    def create_single_report(in_path: str, out_path: str, dictionary: Dict[str, str]) -> None:
        """
        Replaces keys that appear in "in_file" with their corresponding values.
        :param in_path: Path to original word file.
        :param out_path: Path to result word file.
        :param dictionary: Format - Dict[key, [file, value]]
        :return: None.
        """
        # in_path = "C:/Users/TLP-280/PyCharmProjects/Magdad/Magdad/web_features/tech_miun_temp/report_creation/input.docx"
        # out_path = "C:/Users/TLP-280/PyCharmProjects/Magdad/Magdad/web_features/tech_miun_temp/report_creation/output.docx"

        # Open the Word document
        doc: docx.Document = docx.Document(in_path)
        # Loop through all paragraphs in the document
        for para in doc.paragraphs:
            # Loop through keys in the dictionary
            for key, value in dictionary.items():
                # Check if the key is in the paragraph
                if key in para.text:
                    # Replace all instances of key with value
                    para.text = para.text.replace(key, value)

        # Loop through all tables in the document
        for table in doc.tables:
            # Loop through all cells in the table
            for row in table.rows:
                for cell in row.cells:
                    for key, value in dictionary.items():
                        # Check if the key is in the cell
                        if key in cell.text:
                            # Replace all instances of key with value
                            cell.text = cell.text.replace(key, value)

        # Save the modified document as a new file
        doc.save(out_path)

    @staticmethod
    def get_field_list(file: FileTree) -> List[str]:
        """
        Returns a list of strings of all fields in a specific file
        """
        update_file(file)
        df: pd.DataFrame = open_file(file)
        fields = [str(i) for i in df]
        return fields
