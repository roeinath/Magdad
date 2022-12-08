from __future__ import annotations

from mongoengine import *

from APIs.TalpiotAPIs.Group.commanded_group import CommandedGroup
from APIs.TalpiotAPIs.Group.division_group import DivisionGroup


class TeamGroup(CommandedGroup):
    division: DivisionGroup = ReferenceField(DivisionGroup)
