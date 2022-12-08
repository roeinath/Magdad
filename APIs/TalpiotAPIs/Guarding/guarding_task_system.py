from mongoengine import *
from APIs.TalpiotAPIs.Guarding.task_system import TaskSystem
from APIs.TalpiotAPIs.Guarding.task_event import TaskEvent
from APIs.TalpiotAPIs.Guarding.task_type import TaskType


class GuardingTaskSystem(TaskSystem):
    almashType = ReferenceField(TaskType)

    def task_event_updated(self, task_event: TaskEvent):
        #  Get latest amlash type
        try:
            # TODO: Add type to the TaskEvent and filter
            #   by almash type
            latest = TaskEvent.objects(
                system=self,
                data__endTime__lt=task_event.data.endTime
            ).order_by(
                '-data__endTime'
            )[0]

            # TODO: Update latest's participants with the new participants
            #   from the task_event
        except DoesNotExist:
            pass
