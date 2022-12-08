import datetime

from mongoengine import Document, StringField, DateField, ReferenceField, ListField

import web_features.logistic_events.permissions as permissions
from web_framework.server_side.infastructure.constants import *
from APIs.ExternalAPIs import FileToUpload, GoogleDrive
from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.LogisticEvents.logistic_event import LogisticEvent
from APIs.TalpiotAPIs.LogisticEvents.logistic_event_missions import LogisticEventMission
from APIs.TalpiotAPIs.LogisticEvents.logistic_event_status import LogisticEventStatus, LogisticEventStatusOptions
from web_framework.server_side.infastructure.components.confirmation_button import ConfirmationButton
from web_framework.server_side.infastructure.components.display_files import DisplayFile
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanelColumn
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page


class ManageLogisticStatuses(Page):
    @staticmethod
    def get_title() -> str:
        return "ניהול סטטוסי אירועים"

    @staticmethod
    def is_authorized(user: User):
        return permissions.is_user_admin(user)

    def __init__(self, params):
        super().__init__()
        self.sp = StackPanel([])
        self.popup = None
        self.user = None

    def get_page_ui(self, user):
        self.user = user
        self.draw()
        return self.sp

    def draw(self):
        self.sp.clear()

        table: DocumentGridPanel = DocumentGridPanel(LogisticEventStatusOptions, [
            DocumentGridPanelColumn('status_name', 'שם הסטטוס'),
            DocumentGridPanelColumn('permitted_users', 'מי מאשר'),
            DocumentGridPanelColumn('deadline_weeks_before', 'כמה שבועות לפני האירוע')
        ], order_by=['-deadline_weeks_before'])

        table.add_column(lambda option: StackPanel([
            Button("עריכה", lambda: self.add_or_edit_new_option(option)),
            ConfirmationButton("מחיקה", lambda: option.delete(), bg_color='red')
        ], orientation=HORIZONTAL))

        self.sp.add_component(Label("ניהול סטטוסי אירועים אפשריים", size=SIZE_EXTRA_LARGE))
        self.sp.add_component(table)

        self.sp.add_component(Button("יצירת סטטוס אפשרי חדש", self.add_or_edit_new_option))

    def add_or_edit_new_option(self, current_value: LogisticEventStatusOptions = None):
        def save_option(new_option: LogisticEventStatusOptions):
            if current_value:
                current_value.status_name = new_option.status_name
                current_value.permitted_users = new_option.permitted_users
                current_value.deadline_weeks_before = new_option.deadline_weeks_before
                current_value.save()
            else:
                new_option.save()
            self.popup.hide()
            self.draw()

        form = JsonSchemaForm(
            LogisticEventStatusOptions,
            value=current_value or LogisticEventStatusOptions(),
            visible=['status_name', 'permitted_users', 'deadline_weeks_before'],
            display_name={
                'status_name': 'שם הסטטוס',
                'permitted_users': 'מי מאשרים',
                'deadline_weeks_before': 'כמה שבועות לפני האירוע אמור לקרות הסטטוס',
            },
            options={'permitted_users': User.objects},
            options_display={'permitted_users': lambda x: x.get_full_name()},
            submit=save_option
        )
        title = "יצירת סטטוס חדש" if current_value else "עריכת סטטוס"
        self.popup = PopUp(form, title=title, is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)
