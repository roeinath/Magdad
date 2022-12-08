# from talpix import *
import datetime

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.Suggestions.bug_report import BugReport
from APIs.TalpiotAPIs.Suggestions.suggestions import Suggestion
from web_features.talpix import permissions
from web_framework.server_side.infastructure.actions import simple_send_message
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.confirmation_button import ConfirmationButton
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanel
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanelColumn
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.constants import *

class FeaturesSuggestions(Page):
    SEVERITIES = {0: 'נמוך', 1: 'בינוני', 2: 'גבוה'}
    PLATFORM = {0: 'TalpiBot', 1: 'TalpiWeb', 2: 'TalpiX'}

    @staticmethod
    def get_title() -> str:
        return "פיצ'רים ובאגים"

    @staticmethod
    def is_authorized(user):
        return MATLAM in user.role  # Only the people of the base

    def __init__(self, params):
        super().__init__()
        self.user = None
        self.sp = None
        self.features_stack = None
        self.bug_stack = None

        self.popup = None

    ###############
    # bug reports #
    ###############

    def bug_report_form(self):
        def insert_bug_report(form_data):
            BugReport.new_bug_report(user=self.user, description=form_data.description,
                                     severity=form_data.severity, date=datetime.datetime.now()).save()
            simple_send_message(f"באג חדש דווח:\n{form_data.description}", user_list=list(User.objects(bot_admin=True)))
            self.popup.hide()
            self.draw_bug_table()

        form = JsonSchemaForm(BugReport, visible=['description', 'severity'], display_name={
            'description': 'תיאור הבאג',
            'severity': 'חומרת הבאג',
        }, placeholder={
            'description': 'תיאור',
            'severity': 'חומרה',
        }, options={
            'severity': list(self.SEVERITIES.values())
        }, options_display={
            'severity': lambda x: x
        }, submit=insert_bug_report)

        self.popup = PopUp(form, title="דיווח על באג", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)
        self.popup.show()

    def draw_bug_table(self):
        def delete_bug_report(bug: BugReport):
            bug.delete()
            self.draw_bug_table()

        self.bug_stack.clear()
        reports_table = DocumentGridPanel(BugReport, [
            DocumentGridPanelColumn('user', 'צוער/ת', lambda _, user: Label(user.name)),
            DocumentGridPanelColumn('description', 'באג'),
            DocumentGridPanelColumn('severity', 'חומרה'),
            DocumentGridPanelColumn('date', 'תאריך'),
        ])
        if permissions.is_user_developer(self.user):
            reports_table.add_column(
                lambda bug: ConfirmationButton("מחק", action=lambda b=bug: delete_bug_report(b))
            )
        self.bug_stack.add_component(reports_table)

    #######################
    # feature suggestions #
    #######################

    def feature_suggestion_form(self):
        def insert_feature_suggestion(form_data):
            Suggestion.new_suggestion(user=self.user, description=form_data.description, platform=form_data.platform,
                                      date=datetime.datetime.now()).save()
            self.popup.hide()
            self.draw_features_table()

        form = JsonSchemaForm(Suggestion, visible=['description', 'platform'], display_name={
            'description': "תיאור הפיצ'ר",
            'platform': 'איפה',
        }, placeholder={
            'description': '...תיאור',
            'platform': 'איפה',
        }, options={
            'platform': list(self.PLATFORM.values())
        }, options_display={
            'platform': lambda x: x
        }, submit=insert_feature_suggestion)

        self.popup = PopUp(form, title="הצעת פיצ'ר", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)
        self.popup.show()

    def draw_features_table(self):
        def delete_feature_suggestion(suggestion: Suggestion):
            suggestion.delete()
            self.draw_features_table()

        self.features_stack.clear()
        feature_table = DocumentGridPanel(Suggestion, [
            DocumentGridPanelColumn('user', 'צוער/ת', lambda _, user: Label(user.name)),
            DocumentGridPanelColumn('description', "פיצ'ר"),
            DocumentGridPanelColumn('platform', 'איפה'),
            DocumentGridPanelColumn('date', 'תאריך'),
        ])
        if permissions.is_user_developer(self.user):
            feature_table.add_column(
                lambda suggestion: ConfirmationButton("מחק", action=lambda s=suggestion: delete_feature_suggestion(s))
            )
        self.features_stack.add_component(feature_table)

    def get_page_ui(self, user):
        self.sp = StackPanel([])
        self.user = user

        self.sp.add_component(Label("זה לא באג, זה פיצ'ר", size=SIZE_EXTRA_LARGE))
        buttons_panel = StackPanel([], orientation=0)
        self.sp.add_component(buttons_panel)
        self.sp.add_component(Label())

        buttons_panel.add_component(Button("הצע פיצ'ר משלך", self.feature_suggestion_form))
        buttons_panel.add_component(Button("דווח על באג", self.bug_report_form))

        self.bug_stack = StackPanel([])
        self.sp.add_component(self.bug_stack)
        self.draw_bug_table()

        self.sp.add_component(Label())  # margin

        self.features_stack = StackPanel([])
        self.sp.add_component(self.features_stack)
        self.draw_features_table()

        return self.sp
