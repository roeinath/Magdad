from typing import List, Type, Dict, Callable, Any, Tuple

from mongoengine import Document

from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent


def default_label_component_parser(row_data, field_data) -> Label:
    return Label(str(field_data))


class DocumentGridPanelColumn:
    def __init__(self, field: str, title: str = None, component_parser: Callable[[Document, Any], UIComponent] = None):
        """

        :param field: field name for column.
        :param title (recommended): the column title
        :param component_parser (optional): a function that parses the row and field
                    example: {'email': lambda row, field_data: Button('לחץ', action=lambda row: send_email(row)),
                                'name': lambda row, field_data: Label(field_data, bg_color='red')}
        """
        self.field = field
        self.title = title or field
        self.component_parser = component_parser or default_label_component_parser


class DocumentGridPanel(GridPanel):
    def __init__(self, document_class: Type[Document], column_list: List[DocumentGridPanelColumn],
                 filter_by: Dict[str, Any] = {}, order_by: List[str] = [], bordered=True, overlay_tooltip=False,
                 bg_color=COLOR_TRANSPARENT, row_colors: Dict[int, Tuple[str, str]] = {}
                 ):
        """
        :param document_class: a class inherited from mongoengine Document

        :param filter_by (recommended): a dict for filtering the data from the database.
                    example: {'name': 'יהלי אקשטיין', 'mahzor__in': [41, 42, 43], 'time__gt': datetime.now()}
        :param order_by (optional): a list of string for ordering the table. The format is '+<field>' or '-<field>'.
                    example: ['-mahzor', '+name'] - descending order of mahzor and ascending of name
        :param row_colors (optional): {row_num: (<bg_color>, <fg_color>)} for the each row.
        """
        self.__document_class = document_class
        self.__column_list: List[DocumentGridPanelColumn] = column_list
        self.__data = document_class.objects(**filter_by).order_by(*order_by)
        self.__row_colors = row_colors
        if 0 not in row_colors:
            self.__row_colors[0] = (COLOR_PRIMARY_DARK, 'white')
        super().__init__(row_count=len(self.__data) + 1, column_count=len(self.__column_list), bg_color=bg_color,
                         bordered=bordered, overlay_tooltip=overlay_tooltip)

        self.__validate_data()
        self.__validate_fields()
        self.__add_titles()
        self.__add_grid_data()

    def add_column(self, row_parser: Callable[[Document], UIComponent], title: str = ''):
        """
        Adds a column to the table.
        :param row_parser: A function that receives a document and returns the ui component you want to put in the column
                            the function is needed for passing arguments from the row to the component.
        :param title: an optional title for the column
        :return:
        """
        cols = self.column_count
        self.set_column_count(cols + 1)
        bg_color, fg_color = self.__row_colors[0]
        super().add_component(Label(title, fg_color=fg_color), row=0, column=cols, bg_color=bg_color)
        for i, row in enumerate(self.__data):
            first_field = self.__column_list[0].field
            valid_parser = lambda row_data, field_data: row_parser(row_data)
            component = self.__parse_a_component(valid_parser, row, first_field)
            if not component:
                continue
            super().add_component(component, row=i + 1, column=cols)

    def __add_titles(self):
        for j, column in enumerate(self.__column_list):
            bg_color, fg_color = self.__row_colors[0]
            super().add_component(Label(column.title, fg_color=fg_color), row=0, column=j, bg_color=bg_color)

    def __add_grid_data(self):
        for i, row in enumerate(self.__data):
            for j, column in enumerate(self.__column_list):
                component = self.__parse_a_component(column.component_parser, row, column.field)
                if not component:
                    continue
                bg_color, _ = self.__row_colors.get(i + 1, (COLOR_TRANSPARENT, None))
                super().add_component(component, row=i + 1, column=j, bg_color=bg_color)

    @staticmethod
    def __parse_a_component(component_parser, row, field) -> UIComponent:
        try:
            if not hasattr(row, field):
                return default_label_component_parser(None, '')
            field_attr = getattr(row, field)
            return component_parser(row, field_attr)
        except TypeError as err:
            raise Exception(f"Given parser for field '{field}' is not valid:\n\t{err}")

    def __validate_data(self):
        if len(self.__data) == 0:
            super().add_component(Label("הטבלה ריקה"), row=1, column_span=self.column_count)

    def __validate_fields(self):
        if len(self.__column_list) == 0:
            raise Exception(f"Empty list of columns given")
        invalid_fields = [col.field for col in self.__column_list if col.field not in self.__document_class._fields]
        if len(invalid_fields) == 0:
            return
        raise Exception(f"Fields {invalid_fields} don't exist in the document class '{self.__document_class.__name__}'")

    def add_component(self, *args, **kwargs):
        raise Exception("Can't add a component to a DocumentGridPanel")
