from __future__ import annotations
import datetime
from mongoengine import Document, EmailField, StringField, IntField, ReferenceField, LongField, BooleanField, ListField, \
    DictField, DateField
from enum import Enum
from typing import List

from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs import TagList
from APIs.TalpiotAPIs import Tag

from APIs.TalpiotAPIs.TalpiWiki.wiki_pages.base_wiki_page import BaseWikiPage


class LecturerPage(BaseWikiPage):

    middle = ["background", "lecturer_color", "phone_num", "email", "price", "budget_id"]

    visible = BaseWikiPage.visible_top + middle + BaseWikiPage.visible_bottom
    displayed = BaseWikiPage.displayed_top + middle + ["past_lectures"] + BaseWikiPage.displayed_bottom

    # Content fields
    background: str = StringField(max_length=10000, default="")
    lecturer_color: str = StringField(max_length=10000, default="")
    phone_num: str = StringField(max_length=10000, default="")
    email: str = EmailField(max_length=10000, default="change_placeholder@gmail.com")
    price: str = StringField(max_length=10000, default="")
    budget_id: str = StringField(max_length=10000, default="")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.id)
