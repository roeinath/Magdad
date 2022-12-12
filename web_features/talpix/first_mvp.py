# from general import *
from datetime import datetime, timedelta

from APIs.TalpiotAPIs.Tasks.task import Task
from APIs.TalpiotAPIs.Tasks.task_type import TaskType
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.ui_component import UIComponent

LOG_PATH = r"C:\Users\t8770131\WebstormProjects\talpix\grade_puller.log"


class FIRST_MVP(Page):
    def __init__(self, params={}):
        super().__init__(params)
        self.sp = StackPanel([])

    @staticmethod
    def get_title() -> str:
        return "בדיקה"

    @staticmethod
    def is_authorized(user):
        return user.name == "יהלי אקשטיין"

    def get_page_ui(self, user) -> UIComponent:
        return self.sp
