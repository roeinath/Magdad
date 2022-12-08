from dataclasses import fields

import web_framework.server_side.infastructure.constants as const
from web_framework.server_side.infastructure.components.button import Button
from web_features.tech_miun.report_survey import ReportSurvey
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
import webbrowser

from web_features.tech_miun import permissions
from web_features.tech_miun.malshab_info import MalshabInfo, Malshab


# TODO: add components for assesments
class Web:

    def __init__(self, link):
        self._link = link

    def __call__(self):
        webbrowser.open_new_tab(self._link)


class SagabPage(Page):

    def __init__(self, params):
        super().__init__()
        self.sp = None

    @staticmethod
    def get_title() -> str:
        return 'דף סג"ב'

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_sagab_miun(user)

    def get_page_ui(self, user):
        self.sp = StackPanel([])
        title = Label(text='מילוי הערכות\n סג"ב: ' + user.name, size=const.SIZE_EXTRA_LARGE,
                      fg_color=const.COLOR_PRIMARY_DARK, bold=True)
        self.sp.add_component(title)
        return self.sp