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
        ts = Task.objects(task_type=TaskType.objects.get(description="שמירת בית צרפת"))
        for t in ts:
            start_time: datetime = t.start_time
            if start_time.hour < 16 and start_time.month >= 11:
                self.sp.add_component(Label(start_time))
                t.start_time = start_time + timedelta(days=1)
                t.save()
        return self.sp
