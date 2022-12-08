from __future__ import annotations
from mongoengine import Document, EmailField, StringField, IntField, ReferenceField, LongField, BooleanField, ListField, \
    DictField, DateField, DateTimeField
from enum import Enum
from typing import List

from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.Group.group import Group
from APIs.TalpiotAPIs.TalpiWiki.tag_lists import *

import web_features.talpiwiki.constants as constants
from datetime import datetime, date


class PageType(Document):

    page_type: str = StringField(max_length=1000)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def __str__(self):
        return str(self.page_type)

    def __repr__(self):
        return str(self.page_type)

    def __hash__(self):
        return hash(self.id)


class PageTypeChooser(Document):

    page_types: PageType = ReferenceField(PageType, required=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def __str__(self):
        return str(self.page_types)

    def __repr__(self):
        return str(self.page_types)

    def __hash__(self):
        return hash(self.id)


class BaseWikiPage(Document):
    meta = {"allow_inheritance": True}

    visible_top = ["name", "parents", "children", "last_modified", "writer", "audience", "logistic_tags", "bakara_tags",
                   "content_tags", "drive_dir_id"]
    visible_bottom = ["additional_info"]

    displayed_top = ["search_bar", "header", "name", "explanation", "divider", "control_bar", "parents", "children", "last_modified", "writer",
                     "divider"]
    displayed_bottom = ["logistic_tags", "bakara_tags", "content_tags", "additional_info", "files", "event_data"]

    visible = visible_top + visible_bottom
    displayed = displayed_top + displayed_bottom

    default_user = User(name="יוזר דיפולטבי")
    default_date = date.today()
    default_datetime = datetime.now()

    # Permissions - not yet implemented
    edit_permissions: int = IntField(min_value=constants.ALL_ACCESS,
                                     max_value=constants.SAGAB_ACCESS,
                                     default=constants.ALL_ACCESS)
    read_permissions: int = IntField(min_value=constants.ALL_ACCESS,
                                     max_value=constants.SAGAB_ACCESS,
                                     default=constants.ALL_ACCESS)

    # General Data
    name: str = StringField(max_length=1000, required=True)

    # Meta Data
    writer: List[User] = ListField(ReferenceField(User), default=[])
    last_modified: DateField = DateField(default=default_date)

    # Constant Data
    audience: List[Group] = ListField(ReferenceField(Group), default=[])
    additional_info: str = StringField(max_length=10000, default="")

    # Tags
    parents: List[BaseWikiPage] = ListField(ReferenceField('self'), default=[])
    children: List[BaseWikiPage] = ListField(ReferenceField('self'), default=[])
    content_tags: List[Tag] = ListField(ReferenceField(Tag), default=[])
    logistic_tags: List[Tag] = ListField(ReferenceField(Tag), default=[])
    bakara_tags: List[Tag] = ListField(ReferenceField(Tag), default=[])

    # Google stuff
    calendar_id: str = StringField(max_length=10000, default="")
    drive_dir_id: str = StringField(max_length=10000, default="")

    # Calendar data
    calendar_suggestions: List[str] = ListField(StringField(default=""), default=[])
    event_data: List[dict] = ListField(DictField(default=dict()), default=[])

    events_title: List[str] = ListField(StringField(default=""), default=[])
    events_start: List[DateTimeField] = ListField(DateTimeField(default=default_datetime), default=[])
    events_end: List[DateTimeField] = ListField(DateTimeField(default=default_datetime), default=[])

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
