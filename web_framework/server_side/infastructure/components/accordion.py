from typing import List

import web_framework.server_side.infastructure.ids_manager as ids_manager
import web_framework.server_side.infastructure.request_handlers as request_handlers
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *


class Accordion(UIComponent):
    def __init__(self, children: List[UIComponent] = [], titles: List[str] = [],
                 bg_color="transparent", fg_color="black", size=SIZE_MEDIUM):
        super().__init__(bg_color=bg_color, fg_color=fg_color, size=size)
        self.__children = []
        assert (len(children) == len(titles))
        for component, title in zip(children, titles):
            self.add_component(component, title)

    def render(self):
        return {
            JSON_TYPE: JSON_ACCORDION,
            JSON_ID: self.id,
            JSON_FG_COLOR: self.fg_color,
            JSON_BG_COLOR: self.bg_color,
            JSON_SIZE: self.size,
            JSON_CHILDREN: self.__children,
        }

    def add_component(self, ui_component: UIComponent, title):
        ui_component.session_id = self.session_id
        ui_component.title = title
        # self.__children.append(ui_component)

        self.add_action({
            JSON_ACTION: JSON_add_component,
            JSON_VALUE: {
                JSON_ID: self.id,
                JSON_CHILD: {
                    JSON_COMPONENT: ui_component.render(),
                    JSON_TITLE: title
                }
            }
        })
