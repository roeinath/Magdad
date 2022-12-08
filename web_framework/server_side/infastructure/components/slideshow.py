from web_framework.server_side.infastructure import request_handlers
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent
from typing import List

class Slideshow(UIComponent):
    def __init__(self, children: List[UIComponent] = [], interval:int = 5000):
        super().__init__()
        self.children = []
        self.interval = interval
        for comp in children:
            self.add_component(comp)

    def render(self):
        return {
            JSON_TYPE: JSON_SLIDESHOW,
            JSON_ID: self.id,
            JSON_INTERVAL: self.interval
        }

    def add_component(self, ui_component, index = -1):
        ui_component.session_id = self.session_id
        if index == -1:
            self.children.append(ui_component)
        else:
            self.children.insert(index, ui_component)

        self.add_action({
            JSON_ACTION: JSON_add_component,
            JSON_VALUE: {
                JSON_ID: self.id,
                JSON_CHILD: {
                    "component": ui_component.render()
                }
            }
        })