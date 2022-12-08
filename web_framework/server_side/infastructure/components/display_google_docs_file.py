from web_framework.server_side.infastructure import request_handlers
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent


class GoogleDocsDisplay(UIComponent):
    def __init__(self, url, width='1000vw', height='1000vh'):
        super().__init__()
        self.url = url
        self.width = width
        self.height = height

    def render(self):
        return {
            JSON_TYPE: 'GoogleDocsDisplay',
            JSON_ID: self.id,
            JSON_URL: self.url,
            JSON_HEIGHT: self.height,
            JSON_WIDTH: self.width
        }

    def update_url(self, url):
        self.url = url
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_ID: self.id,
                         JSON_URL: self.url},
        })
