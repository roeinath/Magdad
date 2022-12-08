import datetime

from mongoengine.document import Document
from mongoengine.fields import IntField, ListField, ReferenceField, StringField, DateField, BooleanField

from APIs.TalpiotAPIs.User.user import User
from typing import List


class BugReport(Document):
    meta = {'collection': 'bug_report'}

    user: User = ReferenceField(User)
    description: str = StringField()
    severity: str = StringField()
    date: datetime.date = DateField()

    @staticmethod
    def new_bug_report(user, description, severity, date):
        bug = BugReport()
        bug.user = user
        bug.description = description
        bug.severity = severity
        bug.date = date
        return bug
