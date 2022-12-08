from datetime import date

from web_features.TVs import permissions
from web_framework.server_side.infastructure.components.Image import Image
from web_framework.server_side.infastructure.components.countdown import CountDown
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.slideshow import Slideshow
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.ynet import Ynet
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.ui_component import UIComponent


class TVpage41(Page):
    def __init__(self, params):
        super().__init__()
        self.grid = None

    @staticmethod
    def get_title() -> str:
        return "מחזור מא"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_tv_allowed(user)

    def get_page_ui(self, user) -> UIComponent:
        self.sp = StackPanel(orientation=1)
        self.sp_hor = StackPanel(orientation=0)
        self.images = Slideshow(interval=4000)  # 4 sec

        free_date = date(2022, 8, 4)
        current_date = date.today()
        time_left = free_date - current_date

        self.sp.add_component(Label("עמוד הטלווזיה של מחזור מא", size=SIZE_EXTRA_LARGE))
        self.sp.add_component(self.sp_hor)

        self.sp_hor.add_component(Ynet())
        self.sp_hor.add_component(self.images)
        sp2 = StackPanel([])
        sp2.add_component(Label(f"עוד", size=SIZE_EXTRA_LARGE))
        sp2.add_component(CountDown(free_date))
        sp2.add_component(Label(f"לקבע", size=SIZE_EXTRA_LARGE))
        self.sp_hor.add_component(sp2)

        self.images.add_component(
            Image(url="https://cdn.shopify.com/s/files/1/0192/3894/products/TeddyJeep_1024x1024.jpg?v=1571438511"))
        self.images.add_component(
            Image(url="https://ichef.bbci.co.uk/news/976/cpsprodpb/4C63/production/_117455591_ted1.jpg"))
        self.images.add_component(Image(
            url="https://i5.walmartimages.com/asr/7617e51c-6004-42c1-ae63-006728db4ced_1.e3d0bbf4faa40c0a21af34e4f1d02546.jpeg?odnWidth=undefined&odnHeight=undefined&odnBg=ffffff"))

        return self.sp
