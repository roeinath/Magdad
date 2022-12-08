from typing import List

from web_framework.server_side.infastructure import request_handlers
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent


class ImageSlides(UIComponent):
    def __init__(self, images_src, duration, autoplay=false):
        """
        ImageSlides constructor.
        :param row_count: how much rows
        :param column_count: how much columns
        :param bg_color: grid background color slideImages, duration = 5000, autoplay = false}
        """
        super().__init__()
        self.__images_src: images_src
        self.__autoplay = autoplay
        self.__duration = duration

    def render(self):
        return {JSON_TYPE: JSON_GRIDPANEL,
                JSON_ID: self.id,
                'images_src': self.__images_src,
                'duration': self.__duration,
                JSON_CHILDREN: [],
                JSON_BG_COLOR: self.bg_color,
                }

    def add_component(self, ui_component: UIComponent, row=0, column=0,
                      row_span=1, column_span=1, bg_color=COLOR_TRANSPARENT):

        ui_component.session_id = self.session_id

        ui_component.grid_row = row
        ui_component.grid_column = column
        ui_component.grid_row_span = row_span
        ui_component.grid_column_span = column_span

        self.__children.append(ui_component)

        self.add_action({
            JSON_ACTION: JSON_add_component,
            JSON_VALUE: {JSON_ID: self.id,
                         JSON_CHILD: {
                             JSON_COMPONENT: ui_component.render(),
                             JSON_BG_COLOR: bg_color,
                             "row": row,
                             "column": column,
                             "row_span": row_span,
                             "column_span": column_span,
                         }
                         }
        })

    def delete_component(self, ui_component: UIComponent):
        self.__children.remove(ui_component)
        del ui_component.grid_row
        del ui_component.grid_column
        del ui_component.grid_row_span
        del ui_component.grid_column_span

        self.add_action({
            JSON_ACTION: 'delete_child',
            JSON_VALUE: {
                JSON_ID: self.id,
                JSON_COMPONENT: ui_component.id,
            }
        })


    def get_first_level_children(self):
        return self.__children
