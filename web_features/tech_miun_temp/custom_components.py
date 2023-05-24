import webbrowser
from dataclasses import fields
import json
import os
from typing import *

import pandas as pd
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
from APIs.ExternalAPIs.MiunDrive.MiunDriveAPI import get_list_of_all_data_files, update_file, open_file, FileTree


class FileChoosePopUp(PopUp):
    def __init__(self, on_file_chosen, *params, **kargs):
        sp = self.initialize()
        self.on_file_chosen = on_file_chosen
        super().__init__(sp, *params, **kargs)

    def on_select_combo_box(self, selected_file):
        self.current_file = self.current_file.get_child(selected_file)
        children = self.current_file.get_all_children()
        if (children):
            self.file_combos.append(ComboBox(children,
                                             on_changed=lambda selected_file: self.on_select_combo_box(
                                                 children[int(selected_file)])))
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
        if (children):
            self.file_combos.append(ComboBox(children,
                                             on_changed=lambda selected_file: self.on_select_combo_box(
                                                 children[int(selected_file)])))
        else:
            # print an error
            pass

        self.sp.add_component(self.file_combos[0])

        return self.sp

class FileChoosePopUpCreateReport(PopUp):
    def __init__(self, on_file_chosen, *params, **kargs) -> None:
        sp: StackPanel = self.initialize()
        self.on_file_chosen = on_file_chosen
        super().__init__(sp, *params, **kargs)

    def initialize(self) -> StackPanel:
        self.sp: StackPanel = StackPanel([]) # Parent StackPanel, contains all popup content.
        self.file_combos: List[ComboBox] = [] # List of ComboBoxes displayed in the page

        root: FileTree = get_list_of_all_data_files()
        self.current_file: FileTree = root
        children: List[FileTree] = root.get_all_children()

        if children:
            # If root has children, add a ComboBox with them as options
            self.file_combos.append(ComboBox(children,
                                             on_changed=lambda selected_ind: self.on_select_combo_box(
                                                 children[int(selected_ind)])))
        else:
            # If root has no children, an error occurred
            pass

        self.sp.add_component(self.file_combos[0])
        return self.sp

    def btn_clicked(self):
        self.on_file_chosen(self.current_file)
        self.hide()

    def on_select_combo_box(self, selected_file: FileTree):
        self.current_file: FileTree = self.current_file.get_child(selected_file)
        children = self.current_file.get_all_children()
        if children:
            # If current file has children, add a ComboBox with them as options
            self.file_combos.append(ComboBox(children,
                                             on_changed=lambda selected_ind: self.on_select_combo_box(
                                                 children[int(selected_ind)])))
            self.sp.add_component(self.file_combos[-1])
        else:
            # If current file has no children, add "finish" Button
            btn_choose = Button("בחר\י", action=lambda: self.btn_clicked())
            self.sp.add_component(btn_choose)



































DISPLAY_TYPES: List[str] = ["נתון", "גרף 2 משתנים", "היסטוגרמה"]
NUM_PARAMS: List[int] = [1, 2, 2]

CALC_TYPES: List[str] = ["נתון", "ממוצע", "סכום"]
class DataChoosePopUp(PopUp):
    def __init__(self, on_file_chosen, *params, **kargs) -> None:
        self.display_type_chosen: str = "" # Name of display type chosen
        self.calc_types_chosen: List[str] = [] # List of the calculation types chosen in each column
        self.field_names_chosen: List[str] = [] # List of the chosen field names by col

        self.file_combos: List[List[ComboBox]] = [] # All combo-boxes displayed in the popup
        # Each big list is a column and each sub-list is the combo-boxes inside it
        self.current_files: List[FileTree] = [] # List of the current files in each column

        self.sp_main: StackPanel = self.initialize() # Main StackPanel of the page
        self.grid: GridPanel = None # Main grid
        self.sp_column_list: List[StackPanel] = [] # List of stack-panels, one for each column in the grid

        self.on_file_chosen = on_file_chosen # Func to be run on submit of popup

        super().__init__(self.sp_main, *params, **kargs)

    def initialize(self) -> StackPanel:
        """
        Generates the main stack-panel of the page.
        Inserts initial choose_display_type combo-box into it.
        """
        sp_main: StackPanel = StackPanel([]) # Parent StackPanel, contains all popup content.

        # Add display type combo-box
        cb_display_type: ComboBox =  ComboBox(DISPLAY_TYPES,
                                                   on_changed=lambda selected_ind: self.gen_grid_and_submit(
                                                 int(selected_ind)))
        sp_main.add_component(cb_display_type)

        return sp_main

    def gen_grid_and_submit(self, selected_ind: int) -> None:
        """
        Generates the grid and adds the first row to it.
        Generates submit button.
        """
        # Set display type
        self.display_type_chosen = DISPLAY_TYPES[selected_ind]
        # Generate Grid
        self.grid = GridPanel(1, 5, bordered=True)
        self.sp_main.add_component(self.grid)
        self.add_first_row_to_grid(NUM_PARAMS[selected_ind])

        # Generate submit button
        btn_choose = Button("בחר\י", action=lambda: self.btn_clicked())
        self.sp_main.add_component(btn_choose)


    def add_first_row_to_grid(self, num_cols: int) -> None:
        # Initialize lists that depend on num_cols
        self.current_files = [None] * num_cols
        self.field_names_chosen = [None] * num_cols
        self.calc_types_chosen = [None] * num_cols

        # Create columns with choose_calc_type combo-box
        for col in range(num_cols):
            # Add stack-panel into column
            self.sp_column_list.append(StackPanel([]))
            self.grid.add_component(self.sp_column_list[col], 0, col)

            # Add choose_calc_type combo-box to column stack-panel
            def create_lambda(column):
                """
                Needed so that the on_changed func takes the actual column and not the last clicked.
                """
                return lambda selected_ind: self.add_row_to_column(int(selected_ind), column)
            self.sp_column_list[col].add_component(ComboBox(CALC_TYPES,
                                                  on_changed=create_lambda(col)))


    def add_row_to_column(self, calc_type_ind: int, col: int) -> None:
        # Insert calc_type chosen into list
        self.calc_types_chosen[col] = CALC_TYPES[calc_type_ind]

        # Open root file combobox
        self.file_combos.append([])
        root: FileTree = get_list_of_all_data_files()
        self.current_files[col]: FileTree = root
        children: List[FileTree] = root.get_all_children()

        if children:
            # If root has children, add a ComboBox with them as options
            def create_lambda(column):
                return lambda selected_ind: self.on_select_combo_box(children[int(selected_ind)], column)
            self.file_combos[col].append(ComboBox(children,
                                             on_changed=create_lambda(col)))
        else:
            # If root has no children, an error occurred
            print("Error! Root file has no children.")

        self.sp_column_list[col].add_component(self.file_combos[col][0])

    def on_select_combo_box(self, selected_file: FileTree, column: int):
            self.current_files[column]: FileTree = self.current_files[column].get_child(selected_file)
            children = self.current_files[column].get_all_children()
            if children:
                # If current file has children, add a ComboBox with them as options
                self.file_combos[column].append(ComboBox(children,
                                                         on_changed=lambda selected_ind: self.on_select_combo_box(
                                                             children[int(selected_ind)], column)))
                self.sp_column_list[column].add_component(self.file_combos[column][-1])
            else:
                # If current file has no children, do nothing
                self.display_file_fields(self.current_files[column], column, self.sp_column_list)

    def display_file_fields(self, file: FileTree, col: int, sp_parent: List[StackPanel]):
        # Get field list
        update_file(file)
        df: pd.DataFrame = open_file(file)
        field_names = [str(i) for i in df]
        # Open fields combobox
        cb_field: ComboBox = ComboBox(field_names,
                                      on_changed=lambda ind: self.update_list_fields(field_names[int(ind)], col))
        sp_parent[col].add_component(cb_field)

    def update_list_fields(self, new_val: str, ind: int):
        self.field_names_chosen[ind] = new_val

    def btn_clicked(self):
        # self.on_file_chosen(self.current_file)
        num_params: int = len(self.current_files)
        print("DISPLAY TYPE")
        print(self.display_type_chosen)
        print("CALC TYPES")
        for i in range(num_params):
            print(str(i) + " calc type: " + self.calc_types_chosen[i])
        print("FILE PATHS")
        for i in range(num_params):
            print(str(i) + " file path: " + self.current_files[i].get_full_path())
        print("FIELDS")
        for i in range(num_params):
            print(str(i) + " field: " + self.field_names_chosen[i])
        self.hide()

