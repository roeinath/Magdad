from mongoengine import Document, StringField
from mongoengine.fields import IntField


class TaskType(Document):
    description: str = StringField()
    required_people: int = IntField()
    points: int = IntField()
