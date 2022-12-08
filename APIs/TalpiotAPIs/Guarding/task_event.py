import datetime

from mongoengine import *
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.Guarding.task_system import TaskSystem



class TaskEventData(EmbeddedDocument):
    startTime: datetime.datetime = DateTimeField()
    endTime: datetime.datetime = DateTimeField()
    points: int = IntField()


class TaskEvent(Document):
    """
    This DB model represents a task. It can be either a guarding session or a cleaning session, but
    cannot be more specific than that (further specificity is given by the description field). More spcific
    types of duties are defined in the relevant DBs (guard_task_model, cleaning_task_model).
    The following Enum is to be used in the 'type' field of a Task.
    """

    system: TaskSystem = ReferenceField(TaskSystem, required=True)
    data: TaskEventData = EmbeddedDocumentField(TaskEventData)
    participants: [User] = ListField(ReferenceField(User))
    description: str = StringField(max_length=100)
    calendarId: str = StringField()

