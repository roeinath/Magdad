import datetime
from mongoengine import *
from APIs.TalpiotAPIs.Guarding.task_system import TaskSystem
from APIs.TalpiotAPIs.Guarding.task_type import TaskType


class TaskDaySlot(EmbeddedDocument):
    """
    Represents a slot in a TaskDaySchedule
    """

    TIME_FORMAT = "%H:%M"

    startTime: str = StringField(required=True)
    endTime: str = StringField(required=True)
    taskType: TaskType = ReferenceField(TaskType, required=True)

    @staticmethod
    def create_slot(start: datetime.time, end: datetime.time, type_id: str):
        startTime = start.strftime(TaskDaySlot.TIME_FORMAT)
        endTime = end.strftime(TaskDaySlot.TIME_FORMAT)

        taskType = TaskType.objects.get(id=type_id)
        return TaskDaySlot(
            startTime=startTime,
            endTime=endTime,
            taskType=taskType
        )

    def get_start_time(self) -> datetime.time:
        return datetime.datetime.strptime(self.startTime, TaskDaySlot.TIME_FORMAT).time()

    def get_end_time(self) -> datetime.time:
        return datetime.datetime.strptime(self.endTime, TaskDaySlot.TIME_FORMAT).time()


class TaskDaySchedule(Document):
    """
    This represents a pattern for all the guarding duties in some day. For example, the pattern for a standard day
    includes guarding sessions at 17:00-19:20, 19:20-21:40, etc.
    """

    name: str = StringField(max_length=100)
    system: TaskSystem = ReferenceField(TaskSystem, required=True)
    pattern: [TaskDaySlot] = EmbeddedDocumentListField(TaskDaySlot)
