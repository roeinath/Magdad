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
from APIs.TalpiotAPIs.TalpiWiki.wiki_pages.client_page import ClientPage
from APIs.TalpiotAPIs.Group.group import Group


class ProjectPage(BaseWikiPage):

    middle = ["projectal_tags", "status", "client", "summary", "connection_with_client", "conclusions", "organizers"]

    visible = BaseWikiPage.visible_top + middle + BaseWikiPage.visible_bottom
    displayed = BaseWikiPage.displayed_top + middle + BaseWikiPage.displayed_bottom

    default_client = ClientPage(name="לקוח דיפולטיבי")

    # Dynamic fields
    client: List[ClientPage] = ListField(ReferenceField(ClientPage, default=default_client), default=[])
    summary: str = StringField(max_length=10000, default="")
    connection_with_client: str = StringField(max_length=10000, default="")
    conclusions: List[str] = ListField(StringField(max_length=10000, default=""), default=[])
    organizers: List[User] = ListField(ReferenceField(User), default=[])
    status: str = StringField(max_length=10000, default="אין מידע")
    projectal_tags: List[Tag] = ListField(ReferenceField(Tag), default=[])

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
