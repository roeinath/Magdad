from mongoengine import Document, ReferenceField, BooleanField

from APIs.TalpiotAPIs import User


class ClassifiedNotebook(Document):
    user: User = ReferenceField(User)
    is_locked: bool = BooleanField(default=True)
