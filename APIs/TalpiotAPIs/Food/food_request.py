from datetime import datetime
from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField
from mongoengine.fields import BooleanField, IntField
from typing import List

from APIs.TalpiotAPIs.User.user import User


class FoodRequest(Document):
    """:params from the user"""
    user: str = ReferenceField(User, required=False)
    event: str = StringField()
    date: datetime = DateField()
    hour: str = StringField()
    description: str = StringField()
    FoodLimitations: str = StringField()
    execution: str = StringField()
    equipment: str = StringField()
    comments: str = StringField()
    RelevantAuthorities: bool = BooleanField()

    # statuses: str = ListField(required=False)
    """automatic sets"""
    closed: bool = BooleanField()
    is_reported: bool = BooleanField()
    time: str = StringField()

