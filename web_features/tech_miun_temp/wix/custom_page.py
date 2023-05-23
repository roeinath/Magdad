import webbrowser
from dataclasses import fields
import json
import os
from os import path
import sys


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
from APIs.ExternalAPIs.MiunDrive.MiunDriveAPI import get_list_of_all_data_files, update_file, open_file, \
    get_file_object, open_not_drive_file
from web_features.tech_miun_temp.wix.utils import fetch_fields_dict, ID_names, CUSTOM_PAGES_DIR
from web_features.tech_miun_temp.wix.graph_functions import GRAPH_FUNCTIONS
from web_features.tech_miun_temp.wix.statistics_functions import STATISTICS_FUNCTIONS
from typing import *

CUSTOM_PAGES = os.path.join(path.abspath(__file__), '..', 'כל הכתובות של תלפיות.xlsx')



class CustomPage(Page):
    person_id=0

    def __init__(self, params):
        super().__init__(params)

    def handle_error(exctype, value, traceback):  #TODO: CHECK IF COULD BE USED
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    # Set the global exception handler
    sys.excepthook = handle_error

    @staticmethod
    def get_title() -> str:
        return "עיצוב חופשי"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_estimator_miun(user)

    def fetch_field_column(self, field):
        name_file = field.split(':')[0]
        name_column = field.split(':')[1]
        current_file=self.root
        children = self.root.get_all_children()
        current_file = get_file_object(current_file, name_file)
        update_file(current_file)
        self.df = open_file(current_file)
        return self.df[name_column]


    def fetch_field_values(self,user,root,person_id,field): #TODO erase
        try:
            name_file=field.split(':')[0]
            name_column=field.split(':')[1]
            self.user = user
            self.file_combos = []
            self.current_file = root
            self.files = [root]
            children = root.get_all_children()
            self.current_file = get_file_object(root,name_file)
            update_file(self.current_file)
            self.df = open_file(self.current_file)  # opens file as pandas dataframe
            for id_name in ID_names:
                if(id_name in self.df):
                    print(self.df[self.df[id_name] == person_id])
                    value = self.df.loc[self.df[id_name] == person_id, name_column].iloc[0]
                    print(value)
                    return value
            raise Exception('No ID Field')
        except:
            error_label = Label(text='אחד או יותר מפרטי המידע בקובץ שנבחר בעמוד שגויים, כדאי לבדוק את הקובץ או לפנות לתמיכה מצוות האתר',
                                fg_color=COLOR_PRIMARY_DARK,
                                bold=True, size=SIZE_LARGE)
            error_popup = PopUp(error_label, is_shown=True, is_cancelable=True, title='שגיאה')
            self.sp.add_component(error_popup)

    def return_id(self,number,user):
        self.person_id=int(number)
        self.update_page(user)

    def calculate_func(self, jsonified_function: List[str]):
        try:
            func_name = jsonified_function[0]
            statistic_func = STATISTICS_FUNCTIONS[func_name]
            fields_to_fetch = jsonified_function[1]

            fields_columns = []
            for field_to_fetch in fields_to_fetch:
                fields_columns.append(self.fetch_field_column(field_to_fetch))

            return statistic_func(*fields_columns)
        except:
            error_label = Label(text='אופס, אנחנו עוד לא תומכים באחד החישובים כאן, נסו לבחור עמוד אחר',
                                fg_color=COLOR_PRIMARY_DARK,
                                bold=True, size=SIZE_LARGE)
            error_popup = PopUp(error_label, is_shown=True, is_cancelable=True, title='שגיאה')
            self.sp.add_component(error_popup)

    def draw_graph(self, chartJsComponent, graph_name, parameters_list):
        try:
            plot_func_name = parameters_list[0]
            plot_function = GRAPH_FUNCTIONS[plot_func_name]

            x_json, y_json = parameters_list[1]
            x_value = self.calculate_func(x_json)
            y_value = self.calculate_func(y_json)
            plot_function(chartJsComponent, x_value, y_value, graph_name)
        except:
            error_label = Label(text='אופס, כנראה שלא נבחרו גרפים בעמוד הזה, נסו לבחור עמוד אחר', fg_color=COLOR_PRIMARY_DARK,
                                bold=True, size=SIZE_LARGE)
            error_popup = PopUp(error_label, is_shown=True, is_cancelable=True, title='שגיאה')
            self.sp.add_component(error_popup)

    def update_page(self,user):
        with open(os.path.join(CUSTOM_PAGES_DIR,self.selected_page_name),'r') as f:
            groups_dict = json.load(f)
            root = get_list_of_all_data_files()
            group_names = []
            for group_name, fields_list in groups_dict.items():
                group_names.append(group_name)

                for index, field in enumerate(fields_list):
                    real_value = self.fetch_field_values(user, root, self.person_id, field)
                    self.labels[field].update_text(real_value)

    def update_data(self, groups_dict): #TODO fix
        self.root = get_list_of_all_data_files()
        group_names = []
        group_layouts = []
        self.labels={}
        for group_name, fields_dict in groups_dict['Data'].items():
            group_names.append(group_name)

            group_layout = GridPanel(2, len(list(fields_dict.values())), bg_color=COLOR_PRIMARY_DARK)
            index = 0
            for field_name, field in fields_dict.items():
                group_layout.add_component(Label(field_name, fg_color='White'), 0, index)
                real_value = self.fetch_field_values(self.user, self.root, self.person_id, field)
                self.labels[field]=Label(real_value, fg_color='White')
                group_layout.add_component(self.labels[field], 1, index)   #real_value_dict[field]
                index += 1
            group_layouts.append(group_layout)

        accordion = Accordion(group_layouts, group_names,size=SIZE_LARGE)
        self.custom_stack.add_component(accordion)

    def update_graphs(self, groups_dict):
        horizontal_sp = StackPanel(orientation=HORIZONTAL)
        vertical_sps = [StackPanel(), StackPanel(), StackPanel()]

        graphs_dict = groups_dict['Graphs']
        num_graphs = 0
        for graph_name, graph_parameters_list in graphs_dict.items():
            new_graph = ChartjsComponent(width='500px', height='450px')
            self.draw_graph(new_graph, graph_name, graph_parameters_list)
            vertical_sps[num_graphs % 3].add_component(new_graph)
            num_graphs += 1

        for stack in vertical_sps:
            horizontal_sp.add_component(stack)

        self.sp.add_component(Label(text='גרפים',fg_color=COLOR_PRIMARY_DARK,bold=True,italic=True, size=SIZE_EXTRA_LARGE,width=50))
        self.sp.add_component(horizontal_sp)

    def update_custom_page_opened(self, page_name):
        self.custom_stack.clear()
        self.selected_page_name = page_name
        grid_panel_id= GridPanel(50, 3, bordered=True,bg_color=COLOR_PRIMARY_DARK)
        self.custom_stack.add_component(grid_panel_id)
        #self.cadet_id=self.get_id(user)
        '''
        id_utils = [str(u.click_email).split('@')[0] for u in User.objects()]
        name_utils= [str(u.name) for u in User.objects()]
        '''
        data_df =open_not_drive_file(CUSTOM_PAGES)  #opens the abs path of all the ids and names
        personaln_df=data_df['שם פרטי']
        family_names= data_df['שם משפחה']
        id_df=data_df['תעודת זהות']
        names=[]
        ids=[]
        grid_panel_id.add_component(Label(text='בחרו צוער',fg_color='white',bold=True),0)
        for i in range(len(personaln_df)):
            names.append(str(personaln_df[i])+ ' ' + str(family_names[i]))
            ids.append(id_df[i])
        grid_panel_id.add_component(
            ComboBox(names, on_changed=lambda person_id: self.return_id(ids[int(person_id)],self.user)),1)

        #fetch_fields_dict(root: FileTree, json_dict: dict, candidate_id: int)
        try:
            with open(os.path.join(CUSTOM_PAGES_DIR, page_name),'r') as f:
                groups_dict = json.load(f)
                self.update_data(groups_dict)
                '''
                for i in json:
                    graph= ChartjsComponent()
                    group_layout.add_component(graph_i)
                '''
                self.update_graphs(groups_dict)
        except:
            error_label=Label(text='אופס, כנראה שזה דף לא חוקי, נסו לבחור אחד אחר', fg_color=COLOR_PRIMARY_DARK,bold=True,size=SIZE_LARGE)
            error_popup= PopUp(error_label,is_shown=True,is_cancelable=True,title='שגיאה')
            self.sp.add_component(error_popup)


    def get_page_ui(self, user: User):
        self.user = user
        self.sp = StackPanel([]) 
        self.custom_stack = StackPanel([])
        grid_panel_json=GridPanel(50, 3, bordered=True,bg_color=COLOR_PRIMARY_DARK)
        self.sp.add_component(grid_panel_json)

        custom_pages_files = []
        for file in os.listdir(CUSTOM_PAGES_DIR):
            if file.endswith('.json'):
                custom_pages_files.append(file)
        grid_panel_json.add_component(Label(text='בחרו דף להציג',fg_color='white',bold=True),0)

        grid_panel_json.add_component(
            ComboBox(custom_pages_files, on_changed=lambda chosen_ind: self.update_custom_page_opened(custom_pages_files[int(chosen_ind)]))
            ,1)


        self.sp.add_component(self.custom_stack)
       
        return self.sp

   