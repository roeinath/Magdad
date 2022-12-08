from __future__ import annotations
from mongoengine import IntField, StringField

from APIs.TalpiotAPIs.Group.commanded_group import CommandedGroup


class MahzorGroup(CommandedGroup):
    mahzor_num: int = IntField()
    short_name: str = StringField()
    calendar_id: str = StringField(required=False)


if __name__ == '__main__':
    from settings import load_settings
    from APIs.TalpiotSystem import Vault

    load_settings()
    # Vault.get_vault().connect_to_db()

