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
from APIs.TalpiotAPIs.TalpiWiki.wiki_pages.lecturer_page import LecturerPage
from APIs.TalpiotAPIs.Group.group import Group


class ActivityPage(BaseWikiPage):

    middle = ["summary", "recommendation", "feedback", "organizers"]

    visible = BaseWikiPage.visible_top + middle + BaseWikiPage.visible_bottom
    displayed = BaseWikiPage.displayed_top + middle + BaseWikiPage.displayed_bottom

    # Dynamic fields
    summary: str = StringField(max_length=10000, default="")
    recommendation: str = StringField(max_length=10000, default="")
    feedback: str = StringField(max_length=10000, default="")
    organizers: List[User] = ListField(ReferenceField(User), default=[])

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
