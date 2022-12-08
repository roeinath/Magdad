from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField
import datetime
from APIs.TalpiotAPIs.Group.group import Group
from typing import List
from APIs.TalpiotAPIs.CleaningTasks.cleaning_task import CleaningTask
from APIs.TalpiotAPIs.User.user import User


class CleaningDay(Document):

    date: datetime.date = DateField()
    # kaztar: User = ReferenceField(User)
    cleaning_duties: List[CleaningTask] = ListField(ReferenceField(CleaningTask))

    def day_name(self):
        return "day name"
