import datetime

from mongoengine.document import Document
from mongoengine.fields import IntField, ListField, ReferenceField, StringField, DateField

from APIs.TalpiotAPIs.User.user import User
from typing import List


class DummyTask(Document):

    users: List[User] = ListField(ReferenceField(User))
    description: str = StringField()
    points: int = IntField()
    date: datetime.date = DateField()

