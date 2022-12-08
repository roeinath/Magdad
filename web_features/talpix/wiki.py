# from general import *
import os
from argparse import Action
import urllib.parse
import time

from mongoengine import Document, StringField
from APIs.TalpiotAPIs.Gitlab.gitlab_file_tree import GitlabFileTree
from APIs.TalpiotAPIs.Gitlab.update_file_tree import UpdateFileTree, GitlabAPI
from web_features.talpix import permissions
from web_framework.server_side.infastructure.components.all_components_import import FileTree, CodeEditor, Label, \
    Button, HyperLink, JsonSchemaForm, DocumentGridPanel, DocumentGridPanelColumn, ConfirmationButton,\
    CONFIRMATION_TEXT, PopUp, LogViewer, Markdown
from web_framework.server_side.infastructure.components.stack_panel import StackPanel, HORIZONTAL
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.ui_component import UIComponent
from ide_framework.site_container_side.development_feature import DevelopmentFeature
IDE_PAGE_URI = 'ide'
BASE_TEMPLATE = "bot_features/%s/%s/"


class Wiki(Page):
    def __init__(self, params={}):
        super().__init__(params)
        self.path = None
        if len(params) > 0 and params[0] != 'undefined':
            self.path = params[0]
        self.sp = StackPanel([])
        self.default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"documentation/talpibot_wiki/HOME.md")

    @staticmethod
    def get_title() -> str:
        return "Wiki"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_developer(user)

    def get_page_ui(self, user=None) -> UIComponent:
        self.sp = StackPanel([])
        text = ''
        with open(self.default_path if not self.path else self.path, encoding="utf8") as md_file:
            text += md_file.read() + '\n'
        mark = Markdown(text, size=SIZE_SMALL)
        self.sp.add_component(mark)
        return self.sp
