from mongoengine import *
import datetime

from APIs.TalpiotAPIs import User


class Form(Document):

    name: str = StringField(max_length=100, required=True)
    link: str = StringField(max_length=1000, required=True)
    time: datetime.datetime = DateTimeField(required=True)
    group: str = StringField(max_length=100, required=True)
    creator: User = ReferenceField(User)
    not_filled: [User] = ListField(ReferenceField(User))
    calendar: str = StringField(max_length=1000, required=False)
    # Forms.objects.filter(rnot_filled__contains=user)
