# from general import *

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
from web_framework.server_side.infastructure.components.chartjs_component import ChartjsComponent
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_features.TVs import permissions


class FIRST_MVP(Page):
    def __init__(self, params):
        super().__init__()
        self.grid = None

    @staticmethod
    def get_title() -> str:
        return "בדיקה"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_tv_allowed(user)

    def get_page_ui(self, user) -> UIComponent:
        self.sp = StackPanel([])

        self.sp.add_component(ChartjsComponent(
            type='bar',
            data={
                'labels': ['A', 'B', 'C'],
                'datasets': [
                    {
                        'label': '# Of Computerists',
                        'data': [10, 50, 3]
                    }
                ]
            }
        ))

        return self.sp

        self.grid = GridPanel( 3, 3, bg_color='Blue')
        for i in range(3):
            for j in range(3):
                self.grid.add_component(Button(f"{i*3+j}", bg_color= "Red"), i, j)
        return self.grid

