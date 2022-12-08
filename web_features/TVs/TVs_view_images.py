from mongoengine import *

import web_features.TVs.permissions as permissions
from APIs.TalpiotAPIs.TVS.tv_image_link import TVImageLink
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page


class ViewImages(Page):
    @staticmethod
    def get_title() -> str:
        return "הצגת תמונות בטלוויזיות"

    @staticmethod
    def is_authorized(user):  # who can view
        return permissions.is_user_tv_allowed(user)

    def __init__(self, params):
        super().__init__()
        self.container_table = None
        self.popup = None
        self.reports_stack = None

    def get_page_ui(self, user):
        self.user = user

        self.sp = StackPanel([])

        self.sp.add_component(Label("הצגת תמונות בטלוויזיות", size=SIZE_EXTRA_LARGE))

        self.reports_stack = StackPanel([])
        self.sp.add_component(self.reports_stack)
        self.draw_report_table()

        return self.sp

    def delete_image(self, image_link: TVImageLink):
        image_link.delete()
        self.draw_report_table()

    def draw_report_table(self):
        self.reports_stack.clear()
        tv_links = TVImageLink.objects()

        table = GridPanel(len(tv_links) + 1, 4)
        table.add_component(Label('url'), 0, 0)
        table.add_component(Label("כיתוב"), 0, 1)
        table.add_component(Label("מחזור"), 0, 2)

        self.reports_stack.add_component(table, 0)
        for i, tv_link in enumerate(tv_links):
            table.add_component(Label(tv_link.url), i + 1, 0)
            table.add_component(Label(tv_link.greeting), i + 1, 1)
            table.add_component(Label(tv_link.mahzor), i + 1, 2)

            # if permissions.is_user_tv_allowed(self.user):
            #     table.add_component(Button("מחק", action=lambda tv_link=tv_link: self.delete_image(tv_link)),
            #                                 i+1, 3)
