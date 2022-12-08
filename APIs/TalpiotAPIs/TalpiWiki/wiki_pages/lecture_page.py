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


class LecturePage(BaseWikiPage):

    middle = ["summary", "lecturer", "recommendation", "feedback", "price", "organizers"]

    visible = BaseWikiPage.visible_top + middle + BaseWikiPage.visible_bottom
    displayed = BaseWikiPage.displayed_top + middle + BaseWikiPage.displayed_bottom + ["event_data"]

    default_lecturer = LecturerPage(name="מרצה דיפולטיבי")

    # Dynamic fields
    lecturer: List[LecturerPage] = ListField(ReferenceField(LecturerPage, default=default_lecturer), default=[])
    summary: str = StringField(max_length=10000, default="")
    recommendation: str = StringField(max_length=10000, default="אין מידע")
    feedback: str = StringField(max_length=10000, default="")
    price: str = StringField(max_length=10000, default="")
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
