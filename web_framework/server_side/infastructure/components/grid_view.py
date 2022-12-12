from web_framework.server_side.infastructure.ui_component import UIComponent
from typing import List
from web_framework.server_side.infastructure.constants import *
from typing import List

from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent

VERTICAL = 1
HORIZONTAL = 0


class GridView(UIComponent):
    def __init__(self, cols, rows, col_gap = 5, row_gap = 5, children: List[UIComponent] = [], orientation=VERTICAL, width=None, height=None, padding=(10,10,10,10), max_width = None, max_height = None):
        super().__init__()
        self.__list = []
        self.width = width
        self.height = height
        self.padding = padding
        self.cols = cols
        self.rows = rows
        self.col_gap = col_gap
        self.row_gap = row_gap
        self.max_width = max_width
        self.max_height = max_height
        for comp in children:
            self.add_component(comp)

    def render(self):
        return {JSON_TYPE: 'GridView',
                JSON_ID: self.id,
                JSON_WIDTH: self.width,
                JSON_HEIGHT: self.height,
                'padding': self.padding,
                'cols': self.cols,
                'rows': self.rows,
                'colsGap': self.col_gap,
                'rowsGap': self.row_gap,
                'maxWidth': self.max_width,
                'maxHeight': self.max_height
                }

    def add_component(self, ui_component, index=-1):
        ui_component.session_id = self.session_id
        if index == -1:
            self.__list.append(ui_component)
        else:
            self.__list.insert(index, ui_component)

        self.add_action({
            JSON_ACTION: JSON_add_component,
            JSON_VALUE: {
                JSON_ID: self.id,
                JSON_CHILD: {
                    "component": ui_component.render()
                }
            }
        })

    def delete_component(self, comp):
        print("Deleting: " + str(comp) + " (" + str(type(comp)) + "). Is ui component: " + str(
            isinstance(comp, UIComponent)))
        if isinstance(comp, UIComponent):  # comp is a component, find its index and delete
            for i, curr in enumerate(self.__list):
                if comp == curr:
                    self.delete_component(i)
        else:  # Otherwise comp is a number, delete by index
            temp = self.__list[comp]
            del (self.__list[comp])
            self.add_action({
                JSON_ACTION: JSON_DELETE_CHILD,
                JSON_VALUE: {JSON_ID: self.id,
                             'component': temp.id,
                             }
            })

    def clear(self):
        indexes = list(range(len(self.__list)))
        indexes.reverse()

        for i in indexes:
            self.delete_component(i)
