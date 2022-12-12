# from general import *
import os

from web_features.talpix import permissions
from web_framework.server_side.infastructure.components.all_components_import import Markdown
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.ui_component import UIComponent

UNDEFINED = 'undefined'

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI_DIR = os.path.join(CURRENT_DIR, "talpibot_wiki")

HOME_FILE_NAME = "HOME.md"
DEFAULT_PATH = os.path.join(WIKI_DIR, HOME_FILE_NAME)


class BotWiki(Page):
    def __init__(self, params={}):
        super().__init__(params)
        self.file_name = None
        print(params)
        if len(params) > 0 and params[0] != UNDEFINED:
            self.file_name = params[0]
        self.sp = StackPanel([])

    @staticmethod
    def get_title() -> str:
        return "TalpiBot Wiki"

    @staticmethod
    def is_authorized(user):
        return True

    def get_page_ui(self, user=None) -> UIComponent:
        self.sp = StackPanel([])
        if self.file_name is None:
            self.sp.redirect_page(f'/{HOME_FILE_NAME}')

        self.sp.add_component(Label("שימו לב, חלקים מסוימיים אינם מעודכנים תשאלו את אחראי TalpiX על שינויים שנעשו",
                                    fg_color=COLOR_RED, bold=True))
        self.sp.add_component(Label("\n"))

        file_path = self.get_file_path()
        text = self.get_file_text(file_path)

        mark = Markdown(text, size=SIZE_SMALL)
        self.sp.add_component(mark)
        return self.sp

    def get_file_path(self):
        if self.file_name is not None:
            md_path = os.path.join(WIKI_DIR, self.file_name)
            if os.path.isfile(md_path):
                return md_path

        return DEFAULT_PATH

    @staticmethod
    def get_file_text(file_path):
        with open(file_path, encoding="utf8") as md_file:
            text = md_file.read()

        if file_path != DEFAULT_PATH:
            text += f'\n\n[חזרה לעמוד ראשי]({HOME_FILE_NAME})'
        return text
