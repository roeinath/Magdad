import os

import chardet
import xlrd

from APIs.TalpiotAPIs.AssessmentAPI.Database.files import Files
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.confirmation_button import ConfirmationButton
from web_framework.server_side.infastructure.components.display_google_docs_file import GoogleDocsDisplay
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.getdata.academy_grades_interface import *
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.getdata.skirot_grades_interface import *
from APIs.ExternalAPIs.GoogleDrive.google_drive import GoogleDrive
from web_framework.server_side.infastructure.components.chartjs_component import ChartjsComponent
from web_features.Elements.personal_page.modules.constants import *
import math
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_features.Elements.personal_page.modules.grades_from_moodle import *
from APIs.TalpiotAPIs.AssessmentAPI.tsyunomat.GetDataFromDB import *
from os import chdir
from os.path import abspath, dirname
from web_features.Elements.personal_page.permissions import is_user_captain

from web_features.tech_miun_temp.cadet_classes.utils import *
import pandas as pd



class CadetMiunGrades:
    def __init__(self, user: User, year: int, cadet: str, is_real_data: bool):
        self.user: User = user
        self.year: int = year
        self.cadet: str = cadet
        self.is_real_data = is_real_data

        self.grades_layout: GridPanel = None
        self.popup: PopUp = None

    def get_ui(self):
        self.grades_layout = GridPanel(3, 1, bordered=False)
        self.load_user_from_drive(self.user)
        self.grades_layout.add_component(self.get_grades_table(), 0, 0)
        return self.grades_layout

    @staticmethod
    def load_data_from_csv_or_excel(path):
        """
        creates data table from file in path
        :param path: the path
        :return: DataFrame with the data
        """
        file_extension = os.path.splitext(path)[-1].lower()

        df = None


        if file_extension == '.xlsx':
            df = pd.read_excel(path, header=0, engine='openpyxl')
        elif file_extension == '.xls':
            df = pd.read_excel(path, header=0)
        elif file_extension == '.csv':
            with open(path, 'rb') as rawdata:
                encoding = chardet.detect(rawdata.read(10000))["encoding"]
            df = pd.read_csv(path, header=0, skip_blank_lines=True,
                             skipinitialspace=True, encoding=encoding)

        return df

    def get_grades_table(self):
        """
        pulls the grades and puts them in a table
        :return: GridPanel with grades
        """
        grades, average = get_courses_of_user(self.cadet, self.year, self.is_real_data)

        sort_by_semester = lambda v: v[1]["semester"] if v[1]["semester"] is not None else "A+B"

        grades_gp = GridPanel(len(self.table_data[0]) + 4, len(self.table_titles))

        for i, title in enumerate(self.table_titles):
            grades_gp.add_component(Label(title, size=SIZE_LARGE, fg_color="white"), row=0, column=i,
                                    bg_color=COLOR_PRIMARY_DARK)
            for j, data in enumerate(self.table_data[i]):
                if not data:
                    grades_gp.add_component(Label(text="לא ידוע"), row=j + 1, column=i)
                else:
                    grades_gp.add_component(Label(text=str(data)), row=j + 1, column=i)

        return grades_gp
