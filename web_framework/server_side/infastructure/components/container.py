from typing import Optional

from web_framework.server_side.infastructure.constants import JSON_TYPE, JSON_HEIGHT, JSON_WIDTH, \
    JSON_ACTION, JSON_add_component, JSON_ID, JSON_VALUE, JSON_CHILD, JSON_COMPONENT, JSON_MARGIN, JSON_PADDING
from web_framework.server_side.infastructure.ui_component import UIComponent


class Container(UIComponent):
    def __init__(self, width: str = None, height: str = None,
                 padding: (str, str, str, str) = ('10px', '10px', '10px', '10px'),
                 orientation='row', margin: (str, str, str, str) = ('0px', '0px', '0px', '0px'), justify_content=None,
                 align_items=None):
        super().__init__()
        self.padding: (str, str, str, str) = padding
        self.height: str = height
        self.width: str = width
        self.margin: (str, str, str, str) = margin
        self.orientation = orientation
        self.content: Optional[UIComponent] = None
        self.align_items: str = align_items
        self.justify_content: str = justify_content

    def render(self):
        return {
            JSON_TYPE: 'Container',
            JSON_ID: self.id,
            JSON_WIDTH: self.width,
            JSON_HEIGHT: self.height,
            JSON_PADDING: self.padding,
            JSON_MARGIN: self.margin,
            'orientation': self.orientation,
            'alignItems': self.align_items,
            'justifyContent': self.justify_content
        }

    def set_child(self, component: UIComponent):
        self.add_action({
            JSON_ACTION: JSON_add_component,
            JSON_VALUE: {
                JSON_ID: self.id,
                JSON_CHILD: {
                    JSON_COMPONENT: component.render()
                }
            }
        })
