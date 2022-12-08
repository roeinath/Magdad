# from general import *
import datetime
import os

from mongoengine import *
from mongoengine.context_managers import switch_db
from APIs.TalpiotAPIs.CleaningTasks.cleaning_task import CleaningTask

from APIs.TalpiotAPIs.Tasks.guarding.guarding_day import GuardingDay
from APIs.TalpiotAPIs.Tasks.guarding.guarding_week import GuardingWeek
from APIs.TalpiotAPIs.Tasks.task import Task
from web_features.talpix import permissions
from web_framework.server_side.infastructure.components.code_editor import CodeEditor
from web_framework.server_side.infastructure.components.log_viewer import LogViewer
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanelColumn
from web_framework.server_side.infastructure.components.view_logs import ViewLogs
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.ui_component import UIComponent
from APIs.TalpiotAPIs.CleaningTasks.dummy_cleaning_task import DummyCleaningTask

INITIAL_PATH = '../../../../bot/src/ide_framework/feature_logs/'


class TalpiXLogs(Page):
    def __init__(self, params={}):
        super().__init__(params)
        self.sp = StackPanel([])
        self.logs_path = INITIAL_PATH
        self.ce = CodeEditor(self.logs_path, language='text', theme='terminal')

    @staticmethod
    def get_title() -> str:
        return "לוגים"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_developer(user) or permissions.is_user_elements_developer(user)

    def get_page_ui(self, user) -> UIComponent:
        self.sp = StackPanel([])
        self.draw()
        return self.sp

    def draw(self):
        self.sp.clear()
        if os.path.isfile(self.logs_path):
            self.sp.add_component(Label("LOGS"))
            self.sp.add_component(LogViewer(self.logs_path))
            self.sp.add_component(Button('חזרה', action=self.set_logs_path))
        elif os.path.isdir(self.logs_path):
            files_in_dir = ',\n\t'.join(os.listdir(self.logs_path))
            self.sp.add_component(Label())
            self.ce.text = f"files:{files_in_dir}\n{self.logs_path}"
            self.sp.add_component(self.ce)
            self.sp.add_component(Button('+', action=self.update_path))
        else:
            self.sp.add_component(self.ce)
            self.sp.add_component(Button('+', action=self.update_path))

    def update_path(self):
        self.logs_path = self.ce.get_code()
        self.draw()

    def set_logs_path(self):
        self.logs_path = INITIAL_PATH
        self.draw()
