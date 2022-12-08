from mongoengine import Document, DictField, StringField, ReferenceField, ListField
from mongoengine import DEFAULT_CONNECTION_NAME as DB_ALIAS
from APIs.TalpiotAPIs.Group.group import Group
from APIs.TalpiotAPIs.User.user import User
from typing import List, Optional

from APIs.TalpiotAPIs.AttendanceChecker.missing_reason import MissingReason


# A bot command that should be located in the bot_commands collection
class ScheduledAttendanceChecker(Document):
    meta = {'collection': 'scheduled_attendence_checkers', 'db_alias': DB_ALIAS}

    name: str = StringField()
    group: Group = ReferenceField(Group)
    missings: List[MissingReason] = ListField(ReferenceField(MissingReason))
    event_id: Optional[str] = StringField(required=False)

    def get_missing_reason_if_exists(self, user: User):
        for missing in self.missings:
            if missing.user == user:
                return missing.reason
        return None
