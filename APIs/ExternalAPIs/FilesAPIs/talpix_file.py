import os, uuid
from typing import List
from tokenize import String

from mongoengine import Document, StringField, ReferenceField, ListField

from APIs.TalpiotAPIs.User.user import User

class TalpiXFile(Document):

    filename: str = StringField()
    path_on_server: str = StringField()
    owner: User = ReferenceField(User)
    shared_with: List[User] = ListField(ReferenceField(User))