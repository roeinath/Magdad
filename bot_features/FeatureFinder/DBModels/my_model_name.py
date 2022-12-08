import  datetime
from mongoengine import *
from enum import Enum


# Class for your first DB model. Change this file name, class name and the fields to match your feature name

class MyModelName(Document):

    # Change this example field and add your own fields here
    exampleField: str = StringField(max_length=100)
