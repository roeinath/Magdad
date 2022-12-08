from datetime import datetime
from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField
from mongoengine.fields import BooleanField, IntField
from typing import List

from APIs.TalpiotAPIs.User.user import User


class BuildingFixRequest(Document):
    user: str = ReferenceField(User, required=False)
    building: str = StringField()
    floor: str = StringField()
    room: str = StringField()
    description: str = StringField()
    statuses: str = ListField(required=False)
    closed: bool = BooleanField()
    is_reported:bool = BooleanField()