from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField
import datetime
from APIs.TalpiotAPIs.Group.group import Group
from typing import List
from APIs.TalpiotAPIs.Tasks.task import Task
from APIs.TalpiotAPIs.User.user import User


class GuardingDay(Document):

    date: datetime.date = DateField()
    # kaztar: User = ReferenceField(User)
    guardings: List[Task] = ListField(ReferenceField(Task))

    def day_name(self):
        return "day name"

    @staticmethod
    def get_today_guards() -> set:
        guarding_day: GuardingDay = GuardingDay.objects(date=datetime.date.today()).first()
        today_guards = set()
        for guarding_task in guarding_day.guardings:
            for guard in guarding_task.assignment:
                today_guards.add(guard)
        return today_guards
