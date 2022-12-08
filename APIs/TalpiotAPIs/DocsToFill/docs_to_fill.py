from typing import List

from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField

from APIs.TalpiotAPIs import Group


class DocsToFill(Document):
    name: str = StringField()
    url: str = StringField()
    groups: List[Group] = ListField(ReferenceField(Group), default=None)
