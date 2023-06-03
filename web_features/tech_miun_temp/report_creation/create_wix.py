import copy
import json
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

from web_features.tech_miun_temp.custom_components import MODE_DATA, MODE_GRAPH
from web_features.tech_miun_temp.wix.utils import CUSTOM_PAGES_DIR
import os

ID_NAMES = ['id', 'ID', 'תעודת זהות', 'מספר זהות']

# Result dict keys
GRAPHS = "Graphs"
DATAS = "Datas"
NAME_OF_GROUP = "Name Of Group"

class CreateWixPage(Page):

    def __init__(self, params):
        super().__init__(params)
        self.ti_page_name: TextInput = None  # TextInput with path to output destination

        self.ti_keys: List[TextInput] = []  # List of all TextInputs in the grid
        self.files: List[FileTree] = []  # List of all file paths chosen by user
        self.fields: List[str] = []  # List of all fields chosen by user
        self.rows_created: int = 0  # Number of rows created in the grid
        self.grid: GridPanel = None # Main grid

        self.res_dict: Dict[str, Dict[str, Any]] = {} # Dict of json strings generated
        self.init_res_dict()


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

    def init_res_dict(self) -> None:
        self.res_dict[GRAPHS] = {}
        self.res_dict[DATAS] = {}
        self.res_dict[DATAS][NAME_OF_GROUP] = {}

    def get_page_ui(self, user: User):
        # Initialize user and StackPanel
        self.user = user
        self.sp = StackPanel([])

        # Input path TextInput
        self.ti_page_name = TextInput(text_holder='שם העמוד')
        self.sp.add_component(self.ti_page_name)

        # Horizontal StackPanel
        self.grid = GridPanel(100, 2, bordered=True)
        self.sp.add_component(self.grid)
        self.add_row()

        # Add rows Button
        btn_add_row: Button = Button("הוסף שורה")
        btn_add_row.set_action(action=lambda: self.add_row())
        self.sp.add_component(btn_add_row)

        # Submit button
        btn_submit: Button = Button("צור עמוד")
        btn_submit.set_action(
            action=lambda: self.on_submit())
        self.sp.add_component(btn_submit)

        return self.sp

    def add_row(self) -> None:
        num_row: int = self.rows_created

        # Key TextInput
        ti_key: TextInput = TextInput(text_holder='כותרת')
        self.ti_keys.append(ti_key)

        # File Button
        btn_file: Button = Button("בחר/י הצגה")
        btn_file.set_action(action=lambda: self.open_data_choice_form(num_row))
        self.files.append(None)

        # Field Combobox
        self.fields.append("")

        # Add to grid
        self.grid.add_component(ti_key, num_row, 0)
        self.grid.add_component(btn_file, num_row, 1)

        self.rows_created += 1

    def open_data_choice_form(self, num_row: int) -> None:
        """
        Opens a popup in which user chooses a certain file from the MuinDrive file tree.
        @param num_row: The number of row that called the function.
                        Used to enter the file path into the array in the proper location.
        @param grid: Grid to add pass on to handle_file_chosen
        """
        popup = DataChoosePopUp(
            on_file_chosen=lambda res_list, mode: self.handle_file_chosen(res_list, mode, num_row),
            is_shown=False,
            is_cancelable=True,
            title="בחר/י הצגת נתונים")
        self.sp.add_component(popup)
        popup.show()

    def handle_file_chosen(self, popup_res_list: List[Any], mode: str, num_row: int) -> None:
        # Insert result list into final dict
        if mode == MODE_DATA:
            self.res_dict[DATAS][NAME_OF_GROUP][str(num_row)] = popup_res_list
        if mode == MODE_GRAPH:
            self.res_dict[GRAPHS][str(num_row)] = popup_res_list

        # Replace choose file button with file chosen label
        label_graph_chosen: Label = Label(popup_res_list[0])
        self.grid.add_component(label_graph_chosen, num_row, 1)

    def update_list_fields(self, new_val: str, ind: int) -> None:
        self.fields[ind] = new_val

    def on_submit(self) -> None:
        self.update_dict_values()
        self.dump_dict_into_json()

    def update_dict_values(self) -> None:
        # Update Datas
        datas_dict = copy.deepcopy(self.res_dict[DATAS][NAME_OF_GROUP])
        for key, val in datas_dict.items():
            del self.res_dict[DATAS][NAME_OF_GROUP] [key]
            self.res_dict[DATAS][NAME_OF_GROUP][self.ti_keys[int(key)].text] = val

        # Update Graphs
        graphs_dict = copy.deepcopy(self.res_dict[GRAPHS])
        for key, val in graphs_dict.items():
            del self.res_dict[GRAPHS] [key]
            self.res_dict[GRAPHS][self.ti_keys[int(key)].text] = val

    def dump_dict_into_json(self) -> None:
        new_page_json_path: str = os.path.join(CUSTOM_PAGES_DIR, self.ti_page_name.text)
        with open(f"{new_page_json_path}.json", "w+") as outfile:
            json.dump(self.res_dict, outfile)



    @staticmethod
    def get_field_list(file: FileTree) -> List[str]:
        """
        Returns a list of strings of all fields in a specific file
        """
        update_file(file)
        df: pd.DataFrame = open_file(file)
        fields = [str(i) for i in df]
        return fields

