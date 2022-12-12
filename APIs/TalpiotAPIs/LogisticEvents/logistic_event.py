from datetime import datetime, timedelta
from typing import List
from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField, \
    BooleanField, IntField

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.LogisticEvents.logistic_event_status import LogisticEventStatus, LogisticEventStatusOptions


class LogisticEvent(Document):
    meta = {"allow_inheritance": True}

    event_name: str = StringField()
    event_date: datetime = DateField()
    cadets_in_charge: List[User] = ListField(ReferenceField(User), default=[])
    sagaz_in_charge: List[User] = ListField(ReferenceField(User), default=[])
    sagab_in_charge: List[User] = ListField(ReferenceField(User), default=[])
    current_status: LogisticEventStatus = ReferenceField(LogisticEventStatus, default=None)
    statuses: List[LogisticEventStatus] = ListField(ReferenceField(LogisticEventStatus), default=[])
    drive_folder_id: str = StringField(required=False)
    closed: bool = BooleanField(default=False)

    @staticmethod
    def new_status_from_option(event, status_option: LogisticEventStatusOptions):
        permitted_users = status_option.permitted_users if status_option.permitted_users else event.sagab_in_charge
        deadline = event.event_date - timedelta(weeks=status_option.deadline_weeks_before)

        return LogisticEventStatus(event_name=event.event_name, status_name=status_option.status_name,
                                   permitted_users=permitted_users, deadline=deadline).save()

    def get_current_status(self):
        return self.current_status

    def is_user_permitted(self, user):
        return user in self.cadets_in_charge + self.sagaz_in_charge + self.sagab_in_charge
