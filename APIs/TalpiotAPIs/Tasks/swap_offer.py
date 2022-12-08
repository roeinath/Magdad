from APIs.TalpiotAPIs.Tasks.swap_request import SwapRequest
from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField,BooleanField
import datetime
from APIs.TalpiotAPIs.Group.group import Group
from typing import List
from APIs.TalpiotAPIs.Tasks.task import Task
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.Tasks.swap_request import SwapRequest


class SwapOffer(Document):

    owner:User=ReferenceField(User)
    request:SwapRequest=ReferenceField(SwapRequest)
    one_sided:bool = BooleanField()
    counter_task:Task = ReferenceField(Task)


