from mongoengine.fields import BooleanField, IntField
from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField
from typing import List
from APIs.TalpiotAPIs.User.user import User
from datetime import datetime


class TVImageLink(Document):

    url: str = StringField()
    greeting: str = StringField()
    mahzor: int = IntField()


    @staticmethod
    def new_request(url: str, greeting: str, mahzor: int):
        return TVImageLink(url=url, greeting=greeting, mahzor=mahzor)

