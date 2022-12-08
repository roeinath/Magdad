from typing import Callable

import web_framework.server_side.infastructure.ids_manager as ids_manager
import web_framework.server_side.infastructure.request_handlers as request_handlers
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *


class Divider(UIComponent):
    def __init__(self):
        super().__init__()

    def render(self):
        return {JSON_TYPE: JSON_DIVIDER,  JSON_ID: self.id}
