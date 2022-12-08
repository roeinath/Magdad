from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField
from datetime import datetime
from APIs.TalpiotAPIs.Group.group import Group
from APIs.TalpiotAPIs.User.user import User
from typing import List
from APIs.TalpiotAPIs.Tasks.guarding.guarding_day import GuardingDay


class GuardingWeek(Document):

    first_date: str = StringField()
    days: List[GuardingDay] = ListField(ReferenceField(GuardingDay))
    name: str = StringField()
    kaztar: User = ReferenceField(User)

