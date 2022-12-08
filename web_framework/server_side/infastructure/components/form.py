from typing import List

import web_framework.server_side.infastructure.ids_manager as ids_manager
from web_framework.server_side.infastructure import request_handlers
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent


class Form(UIComponent):
    def __init__(self, obj, visible=[], editable: List = [], display_name={}, placeholder: List = [], submit=None):
        super().__init__()
        self.__obj = obj

        self.__properties = self.__obj_to_dict(obj, visible, editable, display_name, placeholder)

        action = self.encapsulate_form_submit(submit, type(obj))
        if action:
            func_id = ids_manager.gen_action_id(action)
            self.__action = self.submit_to_url(func_id)
        else:
            self.__action = None

        self.visible = visible
        self.editable = editable

    def __obj_to_dict(self, obj, visible, editable, display_name: dict, placeholder):
        obj_dict = obj.to_mongo()
        props = []
        for field in obj_dict:
            name = field
            field_type = type(obj[field]).__name__
            field_display_name = display_name.get(field, name)
            is_editable, is_placeholder, is_visible = True, True, True
            if editable:
                is_editable = field in editable
            if placeholder:
                is_placeholder = field in placeholder
            if visible:
                is_visible = field in visible
            initial_data = obj_dict[field]

            res = {"name": name,
                   "type": field_type,
                   "display_name": field_display_name,
                   "editable": is_editable,
                   "visible": is_visible,
                   "initial_value": initial_data,
                   "is_placeholder": is_placeholder,
                   }
            props.append(res)
        return props

    def render(self):
        return {
            JSON_TYPE: 'Form',
            JSON_ID: self.id,
            JSON_PROPERTIES: self.__properties,
            JSON_ACTION: self.__action
        }

    def update_form(self):
        return {
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_TYPE: 'Form',
                         JSON_ID: self.id,
                         JSON_PROPERTIES: self.__properties,
                         JSON_ACTION: self.__action}
        }
