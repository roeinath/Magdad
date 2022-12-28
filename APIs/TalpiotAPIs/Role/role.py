from __future__ import annotations
import datetime
import json
from enum import Enum

from mongoengine import Document, EmailField, StringField, IntField, ReferenceField, LongField, BooleanField, ListField, DictField, DateField
from typing import List





class Role(Document):
    # RoleCategory
    GENERAL = 0
    ELEMENTS = 1
    DEVELOPER = 2
    MIUN = 3


    name: str = StringField(max_length=100)
    display_name: str = StringField(max_length=100, default="")
    description: str = StringField(max_length=1000, default="")
    category: int = IntField(default=0)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.id)







    
