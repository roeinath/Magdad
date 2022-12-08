from datetime import date

from APIs.TalpiotAPIs.TVS.tv_image_link import TVImageLink
from web_features.TVs import permissions
from web_framework.server_side.infastructure.components.Image import Image
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.slideshow import Slideshow
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.ynet import Ynet
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.ui_component import UIComponent


class TVpage43(Page):
    def __init__(self, params):
        super().__init__()
        self.grid = None
        self.sp1 = None
        self.sp = None
        self.caru = None

    @staticmethod
    def get_title() -> str:
        return "מחזור מג"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_tv_allowed(user)

    def fill_with_images(self):
        tv_images = TVImageLink.objects(mahzor=43)
        for tv_image in tv_images:
            sp2 = StackPanel(orientation=1)
            sp2.add_component(Image(url=tv_image.url, scale=0.6))
            sp2.add_component(Label(tv_image.greeting, size=SIZE_LARGE))
            self.caru.add_component(sp2)

    def get_page_ui(self, user) -> UIComponent:
        self.sp = StackPanel(orientation=1)
        self.sp1 = StackPanel(orientation=0)
        self.caru = Slideshow(interval=4000)

        f_date = date(2024, 7, 29)
        l_date = date.today()
        delta = f_date - l_date

        self.sp.add_component(Label("עמוד הטלוויזיה של מחזור מג", size=SIZE_EXTRA_LARGE))
        self.sp.add_component(self.sp1)
        self.sp1.add_component(Ynet())
        self.sp1.add_component(self.caru)
        self.sp1.add_component(Label(f"עוד {delta.days} ימים לקבע", size=SIZE_LARGE))

        self.fill_with_images()
        return self.sp
