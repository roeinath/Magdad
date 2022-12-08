from typing import List

from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent

SIZE_EXTRA_SMALL = 'xs'
SIZE_SMALL = 'sm'
SIZE_MEDIUM = 'md'
SIZE_LARGE = 'lg'
SIZE_EXTRA_LARGE = 'xl'
class GridPanel(UIComponent):
    def __init__(self, row_count, column_count, bg_color=COLOR_TRANSPARENT, bordered=True, overlay_tooltip=False):
        """
        GridPanel constructor.
        :param children: Doesn't work!!!!!! pass []
        :param row_count: how much rows
        :param column_count: how much columns
        :param bg_color: grid background color
        """
        super().__init__(bg_color=bg_color)
        self.__children: List[UIComponent] = []
        self.__row_count = row_count
        self.__column_count = column_count
        self.__bordered = bordered
        self.__overlay_tooltip = overlay_tooltip

    def render(self):
        return {
            JSON_TYPE: JSON_GRIDPANEL,
            JSON_ID: self.id,
            'row_count': self.__row_count,
            'column_count': self.__column_count,
            JSON_CHILDREN: [],
            JSON_BG_COLOR: self.bg_color,
            JSON_BORDERED: self.__bordered,
            JSON_OVERLAY: self.__overlay_tooltip
        }

    def add_component(self, ui_component: UIComponent, row=0, column=0,
                      row_span=1, column_span=1, bg_color=COLOR_TRANSPARENT, delete_before=False):
        ui_component.session_id = self.session_id

        ui_component.grid_row = row
        ui_component.grid_column = column
        ui_component.grid_row_span = row_span
        ui_component.grid_column_span = column_span

        if delete_before:
            self.remove_component_by_index(row, column, row_span, column_span)

        self.__children.append(ui_component)

        self.add_action({
            JSON_ACTION: JSON_add_component,
            JSON_VALUE: {
                JSON_ID: self.id,
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

    def remove_component_by_index(self, row: int, col: int = 0, row_span: int = 0, col_span: int = 0):
        to_remove = []
        print("children.length", len(self.__children))
        for child in self.__children:
            if child.grid_row in range(row, row + row_span) and child.grid_column in range(col, col + col_span):
                to_remove.append(child)
        for comp in to_remove:
            self.delete_component(comp)
            print("removed", row, col)

    def get_first_level_children(self):
        return self.__children

    @property
    def column_count(self):
        return self.__column_count

    @property
    def row_count(self):
        return self.__row_count

    def set_column_count(self, column_count):
        self.__column_count = column_count

    def set_row_count(self, row_count):
        self.__row_count = row_count

    def clear(self):
        indexes = list(range(len(self.__children)))
        indexes.reverse()

        for i in indexes:
            self.delete_component(self.__children[i])
