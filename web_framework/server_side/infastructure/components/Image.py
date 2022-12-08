from web_framework.server_side.infastructure import request_handlers
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent


class Image(UIComponent):
    def __init__(self, url, scale=1):
        super().__init__()
        self.url = url
        self.scale = scale if scale <= 1 else scale / 100

    def render(self):
        return {
            JSON_TYPE: 'image',
            JSON_ID: self.id,
            JSON_URL: self.url,
            JSON_SCALE: self.scale
        }

    def update_url(self, url):
        self.url = url
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_ID: self.id,
                         JSON_URL: self.url},
        })
