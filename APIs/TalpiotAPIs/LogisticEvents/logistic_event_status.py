from datetime import datetime
from typing import List

from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField, \
    BooleanField, IntField

from APIs.ExternalAPIs import CalendarEvent
from APIs.TalpiotAPIs import User


class LogisticEventStatusOptions(Document):
    status_name: str = StringField()
    permitted_users: List[User] = ListField(ReferenceField(User))
    deadline_weeks_before: int = IntField(default=0)


class LogisticEventStatus(Document):
    event_name: str = StringField()
    status_name: str = StringField()
    permitted_users: List[User] = ListField(ReferenceField(User))
    deadline: datetime = DateField()
    attached_file_link: str = StringField(required=False)
    comments: str = StringField(default='')
    calendar_event: CalendarEvent = ReferenceField(CalendarEvent, default=None)
    approved: bool = BooleanField(default=None)
    relevant: bool = BooleanField(default=True)

    @staticmethod
    def new_status(event_name: str, status_name: str, permitted_users: List[User] = [], deadline: datetime = None,
                   attached_file_link: str = None, comments: str = '', approved: bool = False, relevant: bool = True):
        return LogisticEventStatus(event_name=event_name, status_name=status_name, permitted_users=permitted_users,
                                   deadline=deadline, attached_file_link=attached_file_link, comments=comments,
                                   approved=approved, relevant=relevant)

    def is_user_permitted(self, user):
        return user in self.permitted_users

    def __str__(self):
        return f"{self.event_name} - {self.status_name}"
