from web_framework.server_side.infastructure import request_handlers
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent


class Ynet(UIComponent):
    def __init__(self):
        """
            Ynet component
        """
        super().__init__()

    def render(self):
        return {
            JSON_TYPE: JSON_YNET,
            JSON_ID: self.id,
            JSON_TEXT: self.text,
            JSON_BG_COLOR: self.bg_color,
            JSON_FG_COLOR: self.fg_color,
            JSON_SIZE: self.size
        }
