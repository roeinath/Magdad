from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField
from datetime import datetime
from APIs.TalpiotAPIs.Group.group import Group
from typing import List
from APIs.TalpiotAPIs.CleaningTasks.cleaning.cleaning_day import CleaningDay
from APIs.TalpiotAPIs.User.user import User

class CleaningWeek(Document):

    first_date: str = StringField()
    days: List[CleaningDay] = ListField(ReferenceField(CleaningDay))
    name: str = StringField()
    a_mishmahat: User = ReferenceField(User)#Change creation of week to remember to add this field

