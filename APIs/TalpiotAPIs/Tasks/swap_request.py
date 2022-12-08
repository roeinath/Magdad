from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField,BooleanField
import datetime
from APIs.TalpiotAPIs.Group.group import Group
from typing import List
from APIs.TalpiotAPIs.Tasks.task import Task
from APIs.TalpiotAPIs.User.user import User


class SwapRequest(Document):

    owner:User=ReferenceField(User)
    task_time:datetime=DateTimeField()
    offer:Task=ReferenceField(Task)
    exchanged :bool =BooleanField()

    # DELETE THIS FIELD WHEN BOT IS DEPLOYED
    interested: list = ListField()

# rap220501
