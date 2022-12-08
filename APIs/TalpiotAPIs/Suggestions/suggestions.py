import datetime

from mongoengine.document import Document
from mongoengine.fields import IntField, ListField, ReferenceField, StringField, DateField, BooleanField

from APIs.TalpiotAPIs.User.user import User
from typing import List


class Suggestion(Document):
    meta = {'collection': 'feature_suggestion'}

    user: User = ReferenceField(User)
    description: str = StringField()
    platform: str = StringField()
    date: datetime.date = DateField()

    @staticmethod
    def new_suggestion(user, description, platform, date):
        suggestion = Suggestion()
        suggestion.user = user
        suggestion.description = description
        suggestion.platform = platform
        suggestion.date = date
        return suggestion
