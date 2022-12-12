from __future__ import annotations
from mongoengine import Document, StringField


class FormField(Document):
    """
    This DB model represents a single field in a form.
    A field may be a question, a header, just a paragraph...
    It is not to be used by itself, but is to be inherited,
    by other fields implementing it.
    """
    meta = {'allow_inheritance': True, 'abstract': True}

    field_identifier: str = StringField(db_field='identifier', max_length=100, required=True, unique=True)

    def get_identifier(self):
        return self.field_identifier
