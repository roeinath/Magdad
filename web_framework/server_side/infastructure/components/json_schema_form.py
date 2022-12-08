from typing import List
from mongoengine import *
from dateutil import parser

import web_framework.server_side.infastructure.ids_manager as ids_manager
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent

INPUT_TYPES = {
    BooleanField,
    StringField,
    DateTimeField,
    DateField,
}

NUMERIC_INPUT_TYPES = {
    IntField,
    FloatField,
    LongField,
    DecimalField
}

class JsonSchemaForm(UIComponent):
    def __init__(self, cls,
                 value=None,
                 visible= None,
                 not_editable: List = None,
                 display_name=None,
                 paragraphTexts=[],
                 placeholder: dict = None,
                 options: dict = None,
                 options_display: dict = None,
                 submit=None):
        super().__init__(relative_width='80%')
        self.__cls = cls
        self.__value = value


        action = self.encapsulate_form_submit(submit, cls)
        if action:
            func_id = ids_manager.gen_action_id(action)
            self.__action = self.submit_to_url(func_id)
        else:
            self.__action = None

        self.visible = visible if visible else []
        self.placeholder = placeholder if placeholder else {}
        self.not_editable = not_editable if not_editable else []
        self.display_name = display_name if display_name else {}
        self.options = options if options else {}
        self.options_display = options_display if options_display else {}
        self.paragraphTexts = paragraphTexts

        js, ui = self.get_json_schema()
        self.__properties = {
            'json_schema': js,
            'ui_schema': ui
        }

    def encapsulate_form_submit(self, f, object_type):
        if not f:
            return None
        else:
            def _f(data):
                properties = data[JSON_PROPERTIES]

                fields = {}
                for k, v in object_type._fields.items():
                    if k in ['_cls', 'id']:
                        continue

                    v_type = type(v)

                    if k not in properties:
                        continue

                    fields[k] = properties[k]

                    if v_type in [DateTimeField, DateField]:
                        fields[k] = parser.parse(fields[k])

                    if v_type == ListField:
                        field_type = type(v.field)
                        if field_type == ReferenceField:
                            fields[k] = list(map(
                                lambda x: v.field.document_type.objects(id=x)[0],
                                fields[k]))

                obj_class = object_type
                ret_obj = obj_class(**fields)

                f(ret_obj)

            return _f

    def get_field_json_schema(self, key, value, values: dict):
        ui_schema = {
            "ui:disabled": key in self.not_editable,
            "ui:placeholder": self.placeholder.get(key),
        }
        try:
            if value.paragraph:
                ui_schema["ui:widget"] = "textarea"
                ui_schema["ui:rows"] = 4
        except:
            pass

        ftype = type(value)
        type_name = ftype.__name__.split("Field")[0].lower()

        if ftype == ListField:
            json_schema, ui_schema, required = self.get_field_json_schema(key, value.field, {})

            list_values = values.get(key)
            schemas = []

            if list_values:
                schemas = [self.get_field_json_schema(key, value.field, {key: list_values[i]})[0] for i in range(len(list_values))]

            json_schema = {
                "type": "array",
                "title": self.display_name.get(key),
                "uniqueItems": True,
                "default": [x["default"] for x in schemas],
                "items": json_schema
            }

            return json_schema, ui_schema, value.required

        if ftype == ReferenceField:
            # print("REF", self.options.get(key), key, value, values)

            options = [
                {
                    "type": "string",
                    "title": self.options_display.get(key)(x),
                    "enum": [
                        str(x.id)
                    ]
                } for x in self.options.get(key)
            ]

            json_schema = {
                "type": ["string", "null"],
                "anyOf": options + [{"type": "null", "enum": [None], "title": "ללא"}],
                "title": self.display_name.get(key),
                "default": str(values.get(key).id) if key in values and values.get(key) is not None else None
            }

            return json_schema, ui_schema, value.required

        json_schema = {
            'type': "string",
            'title': self.display_name.get(key),
            "default": values.get(key),
        }

        if key in self.options:
            options = [
                {
                    "type": "string",
                    "title": x,
                    "enum": [x]
                } for x in self.options.get(key)
            ]
            json_schema['anyOf'] = options + [{"type": "null", "enum": [None], "title": "ללא"}]

        if ftype == BooleanField:
            json_schema["type"] = "boolean"
            json_schema["default"] = True if values.get(key) else False
        elif ftype == DateField:
            json_schema["format"] = "date"
            json_schema["default"] = None
            if values.get(key):
                json_schema["default"] = values.get(key).strftime("%Y-%m-%d")
        elif ftype == DateTimeField:
            json_schema["format"] = "date-time"
            json_schema["default"] = None
            if values.get(key):
                json_schema["default"] = values.get(key).strftime("%Y-%m-%dT%H:%M")
        elif ftype in [IntField, LongField]:
            json_schema["type"] = "integer"
        elif ftype == FloatField:
            json_schema["type"] = "number"

        return json_schema, ui_schema, value.required if value else False

    def get_json_schema(self):
        """list all the field in the model
        and in the nested models"""

        ui_schema = {}
        json_schema = {
            "type": "object",
            "required": []
        }

        values = {}
        if self.__value:
            for k, v in self.__cls._fields.items():
                values[k] = self.__value[k]

        fields = {}
        # Go over the visible fields in that order
        for k in self.visible:
            if k in ['_cls', 'id']:
                continue
            v = self.__cls._fields[k]

            if k in self.paragraphTexts:
                v.paragraph = True
            else:
                v.paragraph = False

            json, ui, required = self.get_field_json_schema(k, v, values)

            fields[k] = json
            ui_schema[k] = ui

            if required:
                json_schema["required"].append(k)

        json_schema["properties"] = fields

        return json_schema, ui_schema

    def render(self):
        return {
            JSON_TYPE: 'JsonSchemaForm',
            JSON_ID: self.id,
            JSON_RELATIVE_WIDTH: self.relative_width,
            **self.__properties,
            JSON_ACTION: self.__action
        }

    def update_form(self):
        return {
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_TYPE: 'JsonSchemaForm',
                         JSON_ID: self.id,
                         JSON_PROPERTIES: self.__properties,
                         JSON_ACTION: self.__action}
        }
