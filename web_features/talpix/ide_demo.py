# from general import *
import urllib.parse

from mongoengine import *

from APIs.TalpiotAPIs.Gitlab.update_file_tree import UpdateFileTree
from web_features.talpix import permissions
from web_framework.server_side.infastructure.components.all_components_import import FileTree, CodeEditor, Label, Button, HyperLink
from web_framework.server_side.infastructure.components.stack_panel import StackPanel, HORIZONTAL
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.ui_component import UIComponent

IDE_DEMO_PAGE_URI = 'ide_demo'


class IDEDemo(Page):
    def __init__(self, params={}):
        super().__init__(params)
        self.path = None
        if len(params) > 0 and params[0] != 'undefined':
            self.path = params[0]
        self.sp = StackPanel([])
        self.editor_sp = StackPanel([])
        self.code_editor = CodeEditor()
        self.tree = None

    @staticmethod
    def get_title() -> str:
        return "דמו לIDE"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_developer(user)

    def initiate_code_sp(self, path):
        self.sp.clear()
        self.sp.add_component(Label("IDE", fg_color=COLOR_PRIMARY_DARK, size=SIZE_EXTRA_LARGE))
        self.sp.add_component(Label(f"File: {path}", fg_color=COLOR_PRIMARY, size=SIZE_LARGE))
        self.sp.add_component(HyperLink(f"לחצ/י כדי לקבל קישור",
                                        url=f"{IDE_DEMO_PAGE_URI}/{urllib.parse.quote_plus(path)}"))
        content = UpdateFileTree.get_file_code(path)
        self.code_editor = CodeEditor(content)
        self.sp.add_component(self.code_editor)

        buttons_panel = StackPanel([], orientation=HORIZONTAL)

        if path.endswith('.py'):
            buttons_panel.add_component(Button("שמירה", self.print_code))
            buttons_panel.add_component(Button("הרצה", bg_color='green', action=lambda p=path: self.draw_terminal(p)))
        buttons_panel.add_component(Button("חזרה", bg_color='red', action=self.draw_tree))

        self.sp.add_component(buttons_panel)

    def draw_terminal(self, path):
        self.sp.clear()
        # self.sp.add_component(ViewLogs("https://gist.githubusercontent.com/helfi92/96d4444aa0ed46c5f9060a789d316100/raw/ba0d30a9877ea5cc23c7afcd44505dbc2bab1538/typical-live_backing.log"))
        self.sp.add_component(CodeEditor("כאן יופיעו לוגים...", language='text', theme='terminal'))
        self.sp.add_component(Button("חזרה", bg_color='red', action=lambda: self.initiate_code_sp(path)))

    def draw_tree(self):
        if self.tree is None:
            self.tree = FileTree(action=self.initiate_code_sp)
        self.sp.clear()
        self.sp.add_component(Label("IDE", fg_color=COLOR_PRIMARY_DARK, size=SIZE_EXTRA_LARGE))
        self.sp.add_component(Label("בחר/י קובץ", size=SIZE_LARGE))
        self.sp.add_component(self.tree)

    def get_page_ui(self, user) -> UIComponent:
        self.sp = StackPanel([])
        if self.path:
            self.initiate_code_sp(self.path)
        else:
            self.draw_tree()
        return self.sp

    def print_code(self):
        print("CODE:", self.code_editor.get_code())

