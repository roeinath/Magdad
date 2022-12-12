from typing import Optional, Tuple

from web_framework.server_side.infastructure.constants import JSON_TYPE, JSON_BG_COLOR, JSON_HEIGHT, JSON_WIDTH, \
    JSON_ACTION, JSON_add_component, JSON_ID, JSON_VALUE, JSON_CHILD, JSON_COMPONENT
from web_framework.server_side.infastructure.ui_component import UIComponent
import web_framework.server_side.infastructure.ids_manager as ids_manager


class Card(UIComponent):
    def __init__(self, width: str = None, height: str = None, padding: (float, float, float, float) = (10, 10, 10, 10),
                 bg_color: str = 'white',
                 corner_radius: (float, float, float, float) = (10, 10, 10, 10), grid_start: Tuple[int, int] = None,
                 grid_end: Tuple[int, int] = None):
        super().__init__(bg_color)
        self.shadow: Optional[str] = None
        self.padding: (float, float, float, float) = padding
        self.bg_color: str = bg_color
        self.corner_radius: (float, float, float, float) = corner_radius
        self.height: str = height
        self.width: str = width
        self.content: Optional[UIComponent] = None
        self.grid_start = grid_start
        self.grid_end = grid_end
        self.__title = {'display': False}

    def apply_shadow(self, x_off: str, y_off: str, blur: str, spread: str, color: str, opacity: float):
        self.shadow = f'{x_off} {y_off} {blur} {spread} rgba(0,0,0,{opacity})'

    def render(self):
        return {
            JSON_TYPE: 'Card',
            JSON_ID: self.id,
            JSON_WIDTH: self.width,
            JSON_HEIGHT: self.height,
            'padding': self.padding,
            'shadow': self.shadow,
            JSON_BG_COLOR: self.bg_color,
            'radius': self.corner_radius,
            'grid_start': self.grid_start,
            'grid_end': self.grid_end,
            'title': self.__title
        }

    def add_child(self, component: UIComponent):
        self.add_action({
            JSON_ACTION: JSON_add_component,
            JSON_VALUE: {
                JSON_ID: self.id,
                JSON_CHILD: {
                    JSON_COMPONENT: component.render()
                }
            }
        })

    def title(self, title, display=True, bold=True, size=str, align: str = 'right'):
        self.__title = {
            'display': display,
            'text': title,
            'bold': bold,
            'size': size,
            'align': align
        }
