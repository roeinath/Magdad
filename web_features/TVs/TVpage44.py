from datetime import datetime

from APIs.ExternalAPIs import GoogleDrive
from web_features.TVs import permissions
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.slideshow import Slideshow
from web_framework.server_side.infastructure.components.Image import Image
from web_framework.server_side.infastructure.components.countdown import CountDown
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.ui_component import UIComponent


DRIVE_ID = None


class TVpage44(Page):
    def __init__(self, params):
        super().__init__()
        self.grid = None
        self.sp1 = None
        self.sp = None
        self.caru = None

    @staticmethod
    def get_title() -> str:
        return "מחזור מד"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_tv_allowed(user)

    def get_page_ui(self, user) -> UIComponent:
        self.sp = StackPanel(orientation=HORIZONTAL)
        self.sp1 = StackPanel(orientation=VERTICAL)
        self.caru = Slideshow(interval=6000)

        self.sp1.add_component(Label("מחזור מ\"ד!", size=SIZE_EXTRA_LARGE, fg_color=COLOR_PRIMARY_DARK))
        self.sp1.add_component(Label(f"עוד", size=SIZE_EXTRA_LARGE))
        self.sp1.add_component(CountDown(datetime(2025, 7, 28, hour=1)))
        self.sp1.add_component(Label(f"לקבע", size=SIZE_EXTRA_LARGE))

        self.sp.add_component(self.sp1)
        self.sp.add_component(self.caru)

        files = []
        with GoogleDrive.get_instance() as gd:
            if DRIVE_ID:
                files = gd.list_files(DRIVE_ID, no_folders=True)
                files = files['files']

            for f in files:
                img_url = gd.get_thumbnail_from_id(f)
                self.caru.add_component(Image(url=img_url))

        return self.sp
