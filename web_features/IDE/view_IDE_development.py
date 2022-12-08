from web_framework.server_side.infastructure.components.stack_panel import HORIZONTAL
from web_framework.server_side.infastructure.page import Page
from APIs.TalpiotAPIs import User
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.components.all_components_import import Label, StackPanel, Image, GridPanel
from web_framework.server_side.infastructure.constants import *


class ViewIDE(Page):
    @staticmethod
    def get_title():
        return "בדיקת פיתוח"

    def __init__(self, params):
        super().__init__()
        self.sp = None

    def get_page_ui(self, user: User):
        self.sp = StackPanel([])
        return self.sp
