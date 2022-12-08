from mongoengine import *
from APIs.TalpiotAPIs.Guarding.task_system import TaskSystem


class TaskType(Document):
    """
    This DB model represents a general type of task that is often found in task patterns - such as
    a day guard, night guard, morning clean or evening clean. Associated with it is a type (basically
    guard, clean or other) and a number of points it is worth.
    """

    system: TaskSystem = ReferenceField(TaskSystem, required=True)
    name: str = StringField(max_length=100)
    points: float = FloatField(required=True)
    peopleCount: int = IntField(required=True)

    def __str__(self):
        return "Pattern Entry Type " + self.name + "(" + str(self.points) + " points, " + str(self.peopleCount) + " people)"

