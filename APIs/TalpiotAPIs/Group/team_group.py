from __future__ import annotations
from mongoengine import ReferenceField

from APIs.TalpiotAPIs.Group.commanded_group import CommandedGroup
from APIs.TalpiotAPIs.Group.division_group import DivisionGroup
from APIs.TalpiotAPIs.Group.group import Group
from APIs.TalpiotAPIs.Group.mahzor_group import MahzorGroup


class TeamGroup(CommandedGroup):
    division : DivisionGroup = ReferenceField(DivisionGroup)


