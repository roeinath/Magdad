from typing import List

from mongoengine import ReferenceField, ObjectIdField

from web_framework.server_side.infastructure import request_handlers
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *


class DataGrid(UIComponent):
    def encapsulate_datagrid_submit(self, f, obj_lst):
        if not f:
            return None
        else:
            object_class = type(obj_lst[0])

            def _f3(data):
                print(data)
                objects = data["objects"]
                ret_obj_lst = []
                for object_dict in objects:
                    ret_obj_lst.append(object_class(**object_dict))

                print(ret_obj_lst)
                for i, obj in enumerate(ret_obj_lst):
                    if obj_lst[i].pk is not None:
                        obj.pk = obj_lst[i].pk
                res = f(ret_obj_lst)
                if res:
                    self.add_action(res)

            return f

    def __init__(self, obj_lst, visible=[], editable: List = [],
                 display_name={}, placeholder: List = [], submit=None, buttons: dict = {}):
        super().__init__()
        self.__display_name = {}
        self.__editable = []
        self.__placeholder = []
        self.__visible = []
        self.__obj_lst = obj_lst

        self.__header, self.__objects = self.__obj_lst_to_dict(obj_lst, visible, editable, display_name, placeholder)

        action = self.encapsulate_datagrid_submit(submit, obj_lst)
        self.visible, self.editable = visible, editable

        if action:
            func_id = request_handlers.get_id(action)
            self.__action = self.submit_to_url(func_id)
        else:
            self.__action = None

        self.__buttons = []

        for button in buttons:
            button_action = self.encapsulate_form_submit(button, type(obj_lst[0]))
            if button_action:
                func_id = request_handlers.get_id(button_action)
                button_action = self.submit_to_url(func_id)
            else:
                raise ValueError("Expected a dictionary with function")
            self.__buttons.append({buttons[button]: button_action})

    def __obj_lst_to_dict(self, obj_lst, visible, editable, display_name: dict, placeholder):
        obj_dict = obj_lst[0].to_mongo()
        header = self.parse_object_fields(display_name, editable, obj_dict, placeholder, visible, type(obj_lst[0]))

        objects = []
        for obj in obj_lst:
            new = {}
            result = obj.to_mongo()
            for field in result:
                new[field] = result[field].__str__()
            objects.append(new)

        return header, objects

    def parse_object_fields(self, display_name, editable, obj_dict, placeholder, visible, obj_type):
        props = []
        for field in obj_type._fields:
            name = field
            if name == '_id':
                continue
            if name not in visible and not name == 'buttons':
                continue
            field_type = type(obj_type._fields[field])
            is_editable, is_placeholder, is_visible = True, False, True
            if editable:
                is_editable = field in editable
            if placeholder:
                is_placeholder = field in placeholder
            if visible:
                is_visible = field in visible
            field_display_name = display_name.get(field, name)

            if field_type in [ReferenceField, ObjectIdField]:
                editable = False

            res = {"name": name,
                   "type": field_type.__name__.replace('Field', '').lower(),
                   "display_name": field_display_name,
                   "editable": is_editable,
                   "visible": is_visible,
                   "is_placeholder": is_placeholder,
                   }
            props.append(res)
        return props

    def render(self):
        self.add_action({
            JSON_ACTION: JSON_ADD,
            JSON_VALUE: {JSON_TYPE: 'DataGrid',
                         JSON_ID: self.id,
                         JSON_ACTION: self.__action,
                         'headers': self.__header,
                         'objects': self.__objects,
                         'buttons': self.__buttons}
        })

    def update_objects(self, obj_lst):
        self.__objects = self.__obj_lst_to_dict(obj_lst, self.__visible, self.__editable, self.__display_name,
                                                self.__placeholder)
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_ID: self.id,
                         'objects': self.__objects}
        })
