import webbrowser
from dataclasses import fields
import json
import os
from inspect import signature
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
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.constants import *
from APIs.ExternalAPIs.MiunDrive.MiunDriveAPI import get_list_of_all_data_files, update_file, open_file, FileTree
from web_features.tech_miun_temp.wix.graph_functions import GRAPH_FUNCTIONS
from web_features.tech_miun_temp.wix.statistics_functions import STATISTICS_FUNCTIONS
from web_framework.server_side.infastructure.components.pop_up import PopUp


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
        self.sp: StackPanel = StackPanel([])  # Parent StackPanel, contains all popup content.
        self.file_combos: List[ComboBox] = []  # List of ComboBoxes displayed in the page

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



#######################################################################################################################
NUM_EXTRA_PARAMS_GRAPH_FUNC = 2
NUM_EXTRA_PARAMS_STAT_FUNC = 0

NO_INDEX = -1
NO_GRAPH_TYPE_CHOSEN = "No graph type because in data mode."

MODES: List[str] = ["נתון", "גרף"]
MODE_DATA: str = "נתון"
MODE_GRAPH: str = "גרף"

GRAPH_FUNC_TYPES: List[str] = list(GRAPH_FUNCTIONS.keys())
NUM_PARAMS_GRAPH_FUNC: List[int] = [len(signature(GRAPH_FUNCTIONS[key]).parameters) - NUM_EXTRA_PARAMS_GRAPH_FUNC
                                    for key in GRAPH_FUNC_TYPES]
STAT_FUNC_TYPES: List[str] = list(STATISTICS_FUNCTIONS.keys())
NUM_PARAMS_STAT_FUNC: List[int] = [len(signature(STATISTICS_FUNCTIONS[key]).parameters) - NUM_EXTRA_PARAMS_STAT_FUNC
                                   for key in STAT_FUNC_TYPES]

class DataChoosePopUp(PopUp):
    def __init__(self, on_file_chosen, *params, **kwargs) -> None:
        self.mode: str = ""  # Mode: data or graph
        self.graph_func_chosen: str = NO_GRAPH_TYPE_CHOSEN  # Graphing function (plot, pie...)
        self.stat_funcs_chosen: List[str] = []  # Statistic functions chosen (mean, std...)
        self.field_names_chosen: List[List[str]] = []  # List of the chosen field names by col

        self.file_cbs: List[List[List[ComboBox]]] = []  # All combo-boxes displayed in the popup
        # Structure: main_col, sub_col, row
        self.current_files: List[List[FileTree]] = []  # List of the current files in each column

        self.sp_main: StackPanel = self.initialize()  # Main StackPanel of the page
        self.grid_main: GridPanel = None  # Main grid
        self.sp_cols: List[StackPanel] = []  # List of stack-panels, one for each column in the main grid
        self.sub_grids: List[GridPanel] = [] # List of sub grids, one for each stat-func
        self.sp_sub_cols: List[List[StackPanel]] = [] # List of sub cols. Structure: main_col, sub_col

        self.on_file_chosen = on_file_chosen  # Func to be run on submit of popup

        super().__init__(self.sp_main, *params, **kwargs)

    def initialize(self) -> StackPanel:
        """
        Generates the main stack-panel of the page.
        Inserts initial choose_display_type combo-box into it.
        """
        sp_main: StackPanel = StackPanel([])  # Parent StackPanel, contains all popup content.

        # Add data or graph combo-box
        cb_mode: ComboBox = ComboBox(MODES,
                                     on_changed=lambda selected_ind: self.on_mode_chosen(
                                         int(selected_ind)))
        sp_main.add_component(cb_mode)

        return sp_main

    def on_mode_chosen(self, mode_ind: int):
        self.mode = MODES[mode_ind]
        if self.mode == MODE_DATA:
            self.on_graph_func_chosen()
            return

        # Add graph type combo-box
        cb_graph_type: ComboBox = ComboBox(GRAPH_FUNC_TYPES,
                                           on_changed=lambda selected_ind: self.on_graph_func_chosen(
                                               int(selected_ind)))
        self.sp_main.add_component(cb_graph_type)

    def on_graph_func_chosen(self, selected_ind: int = NO_INDEX) -> None:
        """
        Generates the grid and adds the first row to it.
        Generates submit button.
        """
        # Set display type and generate grid
        if self.mode == MODE_DATA:
            self.generate_main_grid(1)

        elif self.mode == MODE_GRAPH:
            self.graph_func_chosen = GRAPH_FUNC_TYPES[selected_ind]
            self.generate_main_grid(NUM_PARAMS_GRAPH_FUNC[selected_ind])

        # Anyway, generate submit button
        btn_choose = Button("בחר\י", action=lambda: self.btn_clicked())
        self.sp_main.add_component(btn_choose)

    def generate_main_grid(self, num_cols: int) -> None:
        # Add grid to main stack-panel
        self.grid_main = GridPanel(1, 5, bordered=True)
        self.sp_main.add_component(self.grid_main)
        self.add_first_row_to_main_grid(num_cols)

        # Initialize lists that depend on num_cols
        self.stat_funcs_chosen = ["Empty" for _ in range(num_cols)]
        self.field_names_chosen = [[] for _ in range(num_cols)]
        self.file_cbs = [[] for _ in range(num_cols)]
        self.current_files = [[] for _ in range(num_cols)]
        self.sub_grids = [None for _ in range(num_cols)]
        self.sp_sub_cols = [[] for _ in range(num_cols)]


    def add_first_row_to_main_grid(self, num_cols: int) -> None:
        # Create columns with choose_calc_type combo-box
        for col in range(num_cols):
            # Add stack-panel into column
            self.sp_cols.append(StackPanel([]))
            self.grid_main.add_component(self.sp_cols[col], 0, col)

            # Add choose_calc_type combo-box to column stack-panel
            def create_lambda(column):
                """
                Needed so that the on_changed func takes the actual column and not the last clicked.
                """
                return lambda selected_ind: self.on_stat_func_chosen(int(selected_ind), column)

            self.sp_cols[col].add_component(ComboBox(STAT_FUNC_TYPES,
                                                     on_changed=create_lambda(col)))

    def on_stat_func_chosen(self, stat_func_ind: int, main_grid_col: int):
        """IN PROG"""
        # Insert stat_func chosen into list
        self.stat_funcs_chosen[main_grid_col] = STAT_FUNC_TYPES[stat_func_ind]

        # Create sub-grid
        num_cols: int = NUM_PARAMS_STAT_FUNC[stat_func_ind]
        self.generate_sub_grid(num_cols, main_grid_col)

    def generate_sub_grid(self, num_cols: int, main_col_ind: int) -> None:
        """IN PROG"""
        # Initialize lists that depend on sub_grid num_cols
        self.field_names_chosen[main_col_ind] = ["Empty" for _ in range(num_cols)]
        self.file_cbs[main_col_ind] = [[] for _ in range(num_cols)]
        self.current_files[main_col_ind] = [None for _ in range(num_cols)]

        # Generate grid
        self.sub_grids[main_col_ind] = GridPanel(1, 5, bordered=True)
        self.sp_cols[main_col_ind].add_component(self.sub_grids[main_col_ind])

        # Add first grid row
        self.add_first_row_to_sub_grid(num_cols, main_col_ind)

    def add_first_row_to_sub_grid(self, num_cols: int, main_col_ind: int):
        # Create columns with root_file combo-box
        for col in range(num_cols):
            # Add stack-panel into sub cols list
            self.sp_sub_cols[main_col_ind].append(StackPanel([]))
            # Add stack-panel to sub-grid
            self.sub_grids[main_col_ind].add_component(self.sp_sub_cols[main_col_ind][col], 0, col)
            self.add_row_to_col_in_sub_grid(main_col_ind, col)

    def add_row_to_col_in_sub_grid(self, main_col: int, sub_col: int):
        # Open root file combobox
        root: FileTree = get_list_of_all_data_files()
        self.current_files[main_col][sub_col] = root
        children: List[FileTree] = root.get_all_children()

        if children:
            # If root has children, add a ComboBox with them as options
            def create_lambda(main_column, sub_column):
                return lambda selected_ind: self.on_select_combo_box(children[int(selected_ind)], main_column, sub_column)

            self.file_cbs[main_col][sub_col].append(ComboBox(children,
                                                    on_changed=create_lambda(main_col, sub_col)))
        else:
            # If root has no children, an error occurred
            print("Error! Root file has no children.")

        self.sp_sub_cols[main_col][sub_col].add_component(self.file_cbs[main_col][sub_col][0])


    def on_select_combo_box(self, selected_file_ind: FileTree, main_col: int, sub_col: int):
        self.current_files[main_col][sub_col] = self.current_files[main_col][sub_col].get_child(selected_file_ind)
        children = self.current_files[main_col][sub_col].get_all_children()
        if children:
            # If current file has children, add a ComboBox with them as options
            self.file_cbs[main_col][sub_col].append(ComboBox(children,
                                                    on_changed=lambda selected_ind: self.on_select_combo_box(
                                                         children[int(selected_ind)], main_col, sub_col)))
            self.sp_sub_cols[main_col][sub_col].add_component(self.file_cbs[main_col][sub_col][-1])
        else:
            # If current file has no children, do nothing
            self.display_file_fields(self.current_files[main_col][sub_col], main_col, sub_col, self.sp_sub_cols)

    def display_file_fields(self, file: FileTree, main_col: int, sub_col: int, sp_parent: List[StackPanel]):
        # Get field list
        update_file(file)
        df: pd.DataFrame = open_file(file)
        field_names = [str(i) for i in df]
        # Open fields combobox
        cb_field: ComboBox = ComboBox(field_names,
                                      on_changed=lambda ind: self.update_field_names_chosen(field_names[int(ind)], main_col, sub_col))
        sp_parent[main_col][sub_col].add_component(cb_field)

    def update_field_names_chosen(self, new_val: str, main_ind: int, sub_ind: int):
        self.field_names_chosen[main_ind][sub_ind] = new_val

    def btn_clicked(self):
        res_list: List[Any] = self.create_popup_result()
        self.on_file_chosen(res_list, self.mode)
        self.hide()

    def create_popup_result(self) -> List[Any]:
        if self.mode == MODE_DATA:
            # Main scale is on length 1.
            # Iterate over sub-scale.
            params: List[str] = []
            for i in range(len(self.field_names_chosen[0])):
                params.append(f'{self.current_files[0][i].get_full_path()[1:]}:{self.field_names_chosen[0][i]}')
            return [self.stat_funcs_chosen[0], params]

        if self.mode == MODE_GRAPH:
            # Iterate over main scale
            # Iterate also over sub-scale
            stat_funcs_list: List[List[Any]] = []
            params: List[str]
            for i in range(len(self.stat_funcs_chosen)):
                params = []
                for j in range(len(self.field_names_chosen[i])):
                    params.append(f'{self.current_files[i][j].get_full_path()[1:]}:{self.field_names_chosen[i][j]}')
                stat_funcs_list.append([self.stat_funcs_chosen[i], params])
            return [self.graph_func_chosen, stat_funcs_list]





