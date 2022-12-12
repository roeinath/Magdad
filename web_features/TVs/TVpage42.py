from datetime import date, datetime, timedelta

from APIs.ExternalAPIs import GoogleDrive
from web_features.TVs import permissions
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.slideshow import Slideshow
from web_framework.server_side.infastructure.components.ynet import Ynet
from web_framework.server_side.infastructure.components.Image import Image
from web_framework.server_side.infastructure.components.countdown import CountDown
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.ui_component import UIComponent


PUPPY_URLS = {
    "בוגו שיפטן": 'https://i.ibb.co/Tgrn44V/image.jpg',
    "בוץ' אורן": 'https://i.ibb.co/7ykctNp/image.jpg',
    "בנימין מילוא": 'https://i.ibb.co/nQN0Kxy/image.jpg',
    "ברנדי גת": 'https://i.ibb.co/PQ8w7hd/image.jpg',
    "דיזי שפר": 'https://i.ibb.co/M8tWRzx/image.jpg',
    "וונדי קארו": 'https://i.ibb.co/tQbWDwc/image.jpg',
    "חיליק סימיונוביץ'": 'https://i.ibb.co/N14B83r/image.jpg',
    "לאו סימיונוביץ'": 'https://i.ibb.co/F4Tfgjr/image.jpg',
    "סימון סימיונוביץ'": 'https://i.ibb.co/smr5xQ8/image.jpg',
    "פאפי בנגל": 'https://i.ibb.co/qm2Nfgq/image.jpg',
    "פפר קגן": 'https://i.ibb.co/42DN2Qc/image.jpg',
    "צ'אפו קיראל": 'https://i.ibb.co/sKgbwBC/image.jpg',
    "צ'ילי ארן": 'https://i.ibb.co/H4p0TCg/image.jpg',
    "אוליבר טלמור": 'https://i.ibb.co/zZNNvqY/image.png',
    "ביסלי אבירם": 'https://i.ibb.co/S5G10pV/image.png',
    "ג'וי פלוס": 'https://i.ibb.co/ZWwy95Q/image.png',
    "ג'ויה יפה": 'https://i.ibb.co/F8BcqpC/image.png',
    "ג'ולי ליכטשטיין": 'https://i.ibb.co/qCx0Xhp/image.jpg',
    "ג'יני ורשקוב": 'https://i.ibb.co/GHLtsR9/image.png',
    "טופי וקסמן": 'https://i.ibb.co/3B2T1Hr/image.png',
    "לאקי טלמור": 'https://i.ibb.co/KbZ5nKh/image.png',
    "לוקה דיין": 'https://i.ibb.co/QMM7Dw6/image.png',
    "מייפל כהן": 'https://i.ibb.co/BfHGXjP/image.png',
    "סופר איידול 105": 'https://i.ibb.co/1nkF2Dc/105.png',
    "סימבה שפר": 'https://i.ibb.co/MVV4Jvx/image.png',
    "אבשלום וגדעון עציון": 'https://i.ibb.co/pn85rfd/image.png',
    "צ'יקה ישפה": 'https://i.ibb.co/q1BZk9F/image.png',
    "קים טלמור": 'https://i.ibb.co/mTwGdh9/image.png',
    "תיקו וגמזו אורן": 'https://i.ibb.co/n1DxFdr/image.png',
    "ליאו פוקס": "https://i.ibb.co/DYcGg1J/dad706da-3452-40ce-9990-f9c0a98ddd94.jpg"
}


DRIVE_ID = "13ftcoq65DRAozFShYms60h9SXjOSeHvN"


class TVpage42(Page):
    def __init__(self, params):
        super().__init__()
        self.grid = None
        self.sp1 = None
        self.sp = None
        self.caru = None

    @staticmethod
    def get_title() -> str:
        return "מחזור מב"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_tv_allowed(user)

    def get_page_ui(self, user) -> UIComponent:
        self.sp = StackPanel(orientation=HORIZONTAL)
        self.sp1 = StackPanel(orientation=VERTICAL)
        self.caru = Slideshow(interval=6000)

        self.sp1.add_component(Label("מחזור מ\"ב - הכי טוב!", size=SIZE_EXTRA_LARGE, fg_color=COLOR_PRIMARY_DARK))
        self.sp1.add_component(Label(f"עוד", size=SIZE_EXTRA_LARGE))
        self.sp1.add_component(CountDown(datetime(2023, 8, 13, hour=1)))
        self.sp1.add_component(Label(f"לקבע", size=SIZE_EXTRA_LARGE))

        self.sp.add_component(self.sp1)
        self.sp.add_component(self.caru)

        with GoogleDrive.get_instance() as gd:
            files = gd.list_files(DRIVE_ID, no_folders=True)
            for f in files['files']:
                img_url = gd.get_thumbnail_from_id(f)
                self.caru.add_component(Image(url=img_url))


        # num_of_puppies = 20
        # response = requests.get(f'https://dog.ceo/api/breeds/image/random/{num_of_puppies}').json()
        # puppies = response['message']
        # for puppy_url in puppies:
        #     self.caru.add_component(Image(url=puppy_url, scale=0.6))

        # for name, puppy_url in PUPPY_URLS.items():
        #     pup_sp = StackPanel(orientation=1)
        #     pup_sp.add_component(Label(name, size='xl'))
        #     pup_sp.add_component(Image(url=puppy_url, scale=90))
        #     self.caru.add_component(pup_sp)

        return self.sp
