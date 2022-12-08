import datetime

from APIs.TalpiotAPIs import User
from mongoengine import *
from enum import Enum


# Class for your first DB model. Change this file name, class name and the fields to match your feature name

class OrderEquipment(Document):
    # Change this example field and add your own fields here
    # exampleField: str = StringField(max_length=100)
    mahzor: int = IntField()
    quantity: int = IntField()
    product: int = IntField()
    status: bool = StringField()
