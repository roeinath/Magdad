from mongoengine import *

import web_features.shagmach.permissions as permissions
from APIs.TalpiotAPIs import Group
from APIs.TalpiotAPIs.DocsToFill.docs_to_fill import DocsToFill
from APIs.TalpiotAPIs.Shagmach.blay_request import ItemFixRequest, ItemTypes
from web_framework.server_side.infastructure.components.display_google_docs_file import GoogleDocsDisplay
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
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page


class ViewDocsToFill(Page):
    @staticmethod
    def get_title() -> str:
        return "דוקים"

    @staticmethod
    def is_authorized(user):  # who can view
        return permissions.is_user_admin(user)  # 'everyone can view'

    def __init__(self, params):
        super().__init__()
        self.sp = StackPanel([])

        self.accordion = Accordion()
        self.popup = None
        self.user = None

    def get_page_ui(self, user):
        self.user = user

        self.sp.add_component(Label("דוקים שימושיים", size=SIZE_EXTRA_LARGE))
        if permissions.is_user_admin(user):
            self.sp.add_component(Button("הוסף דוק", self.create_doc))

        self.sp.add_component(self.accordion)
        for doc in DocsToFill.objects:
            self.accordion.add_component(GoogleDocsDisplay(doc.url, width='2000vw'), doc.name)
        return self.sp

    def create_doc(self):
        def save_doc(doc):
            doc.save()
            self.popup.hide()

        form = JsonSchemaForm(
            DocsToFill,
            visible=['name', 'url', 'groups'],
            display_name={
                'name': 'שם הדוק',
                'url': 'קישור',
                'groups': 'קבוצות עם הרשאות'
            },
            placeholder={
                'name': 'שם...',
                'url': 'לדוגמא: https://docs.google.com/spreadsheets/d/.../edit'
            },
            options={
                'groups': Group.objects
            },
            options_display={
                'groups': lambda x: x.name
            },
            submit=save_doc
        )

        self.popup = PopUp(form, title="הוספת דוק", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)
