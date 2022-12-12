from typing import List, Callable, Dict
from mongoengine import *
from dateutil import parser

import web_framework.server_side.infastructure.ids_manager as ids_manager
from APIs.TalpiotAPIs.Forms.questions.question import Question
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent
from APIs.TalpiotAPIs import NewForm, FormField

from DateTime import DateTime

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

# TODO: change of the values to be included in the field's document


class JsonSchemaNewForm(UIComponent):
    def __init__(self, form_doc : NewForm,
                 value=None,
                 visible=None,
                 not_editable: List = None,
                 display_name=None,
                 paragraph_texts=[],
                 placeholder: dict = None,
                 options: dict = None,
                 options_display: dict = None,
                 submit: Callable[[Dict[str, any]], None] = None):
        """
        Generates a form from a NewForm document.
        :param form_doc: The document itself
        :param value: Dictionary of default values for fields. {field_identifier: default_value}
        :param visible: List of fields to be shown on the form. [field_identifier#1, field_identifier#2, ...]
        :param not_editable: List of non-editable fields. [field_identifier#1, field_identifier#2, ...]
        :param display_name: Dictionary of fields display-name. {field_identifier: display_name}
        :param paragraph_texts:
        :param placeholder: Dictionary of placeholders for fields. {field_identifier: placeholder}
        :param options:
        :param options_display:
        :param submit: Submit function, receives dict of {field_identifier: value} on submit.
        """
        super().__init__(relative_width='80%')
        self.__form_doc = form_doc
        self._value = value

        action = self.encapsulate_form_submit(submit, form_doc)
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
        self.paragraphTexts = paragraph_texts

        js, ui = self.get_json_schema()
        self.__properties = {
            'json_schema': js,
            'ui_schema': ui
        }

    def encapsulate_form_submit(self, f, form_doc: NewForm):
        if not f:
            return None
        else:
            def _f(data):
                properties = data[JSON_PROPERTIES]
                values = {}

                for field in form_doc.fields:
                    # if k not in properties:
                    #     continue

                    values[field.field_identifier] = properties[field.field_identifier]

                    if isinstance(field, Question):
                        # It's a question and can receive input
                        question: Question = field
                        v_type = question.get_answer_type()

                        if v_type in [DateTime]:
                            values[field.field_identifier] = parser.parse(values[field.field_identifier])

                f(values)

            return _f

    def get_field_json_schema(self, field: FormField, values: dict):
        ui_schema = {
            "ui:disabled": field.field_identifier in self.not_editable,
            "ui:placeholder": self.placeholder.get(field.field_identifier),
        }
        if isinstance(field, Question):
            json_schema = {
                'type': "string",
                'title': field.get_question(),
                "default": values.get(field.field_identifier),
            }

            ftype = field.get_answer_type()
            if ftype == bool:
                json_schema["type"] = "boolean"
                json_schema["default"] = True if values.get(field.field_identifier) else False
            elif ftype == DateTime:
                json_schema["format"] = "date"
                json_schema["default"] = None
                if values.get(field.field_identifier):
                    json_schema["default"] = values.get(field.field_identifier).strftime("%Y-%m-%d")
            # elif ftype == DateTimeField:
            #     json_schema["format"] = "date-time"
            #     json_schema["default"] = None
            #     if values.get(key):
            #         json_schema["default"] = values.get(key).strftime("%Y-%m-%dT%H:%M")
            elif ftype in [int]:
                json_schema["type"] = "integer"
            elif ftype == float:
                json_schema["type"] = "number"

            field_options = field.options()
            if field_options is not None and len(field_options) > 0:
                # It has options
                options = [
                    {
                        "type": "string",
                        "title": option,
                        "enum": [field_options[option]]
                    } for option in field_options.keys()
                ]
                json_schema['anyOf'] = options
                if not values.get(field.field_identifier):
                    json_schema['default'] = list(field_options.keys())[0]
        else:
            raise NotImplementedError('Non question fields are currently not implemented')

        return json_schema, ui_schema

    def get_json_schema(self):
        """list all the field in the model
        and in the nested models"""

        ui_schema = {}
        json_schema = {
            "type": "object",
            "required": []
        }

        values = {}
        if self._value:
            for field in self.__form_doc.fields:
                values[field.field_identifier] = self._value.get(field.field_identifier)

        json_schemas = {}
        # Go over the visible fields in that order
        for field_identifier in self.visible:

            field = self.__form_doc.get_field_by_identifier(field_identifier)

            # if k in self.paragraphTexts:
            #     v.paragraph = True
            # else:
            #     v.paragraph = False

            json, ui = self.get_field_json_schema(field, values)

            json_schemas[field_identifier] = json
            ui_schema[field_identifier] = ui

            # if field.is_:
            #     json_schema["required"].append(k)

        json_schema["properties"] = json_schemas

        return json_schema, ui_schema

    def render(self):
        return {
            JSON_TYPE: 'JsonSchemaForm',
            JSON_ID: self.id,
            JSON_RELATIVE_WIDTH: self.relative_width,
            **self.__properties,
            JSON_ACTION: self.__action
        }

    def change_form(self, form):
        self.__form_doc = form
        self.update_form()

    def update_form(self):
        js, ui = self.get_json_schema()
        self.__properties = {
            'json_schema': js,
            'ui_schema': ui
        }
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {JSON_TYPE: 'JsonSchemaForm',
                         JSON_ID: self.id,
                         JSON_PROPERTIES: self.__properties,
                         JSON_ACTION: self.__action}
        })

    @property
    def value(self):
        return self._value
