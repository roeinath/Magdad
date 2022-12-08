from mongoengine import *
from APIs.TalpiotAPIs.Group.group import Group


class TaskSystem(Document):
    """
    This DB model represents a task system. Every separate
    task system contains different taskEvents, daySchedules,
    and taskTypes.
    """
    meta = {'allow_inheritance': True}

    name: str = StringField(required=True)
    calendarId: str = StringField()
    groups: [Group] = ListField(ReferenceField(Group))

    GROUP_COLORS = [
        "red",
        "darkblue",
        "lime",
        "purple",
        "yellow",
        "maroon",
        "olive",
        "magneta"
    ]

    def task_event_updated(self, task_event):
        pass
