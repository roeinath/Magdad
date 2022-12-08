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


class YearPage(BaseWikiPage):

    middle = ["core_values", "goals", "logic_line", "organizers", "responsibilities"]

    visible = BaseWikiPage.visible_top + middle + ["calendar_id"] + BaseWikiPage.visible_bottom
    displayed = BaseWikiPage.displayed_top + middle + ["output_calendar", "omes_grid"] + BaseWikiPage.displayed_bottom

    # Content fields
    core_values: List[str] = ListField(StringField(max_length=10000, default=""), default=[])
    goals: List[str] = ListField(StringField(max_length=10000, default=""), default=[])
    logic_line: str = StringField(max_length=10000, default="")         # organizing idea
    organizers: List[User] = ListField(ReferenceField(User), default=[])
    responsibilities: List[str] = ListField(StringField(max_length=10000, default=""), default=[])

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
