from datetime import datetime
from typing import List

from mongoengine import Document, ReferenceField, ListField, StringField, DateField, BooleanField

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.LogisticEvents.logistic_event import LogisticEvent


class LogisticEventObject(Document):
    meta = {'allow_inheritance': True}

    event_name: str = ReferenceField(LogisticEvent)
    description: str = StringField()
    users_in_charge: List[User] = ListField(ReferenceField(User))
    deadline: datetime = DateField()
    comments: str = StringField(default='')
    approved: bool = BooleanField(default=None)

    @staticmethod
    def new_mission(logistic_event: LogisticEvent, description: str, users_in_charge: List[User] = [],
                    deadline: datetime = None, comments: str = '', approved: bool = False):
        return LogisticEventObject(logistic_event=logistic_event, description=description,
                                   users_in_charge=users_in_charge, deadline=deadline,
                                   comments=comments, approved=approved)

    def is_user_permitted(self, user):
        return user in self.users_in_charge
