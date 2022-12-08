from __future__ import annotations
from mongoengine import ReferenceField

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.Group.group import Group


class CommandedGroup(Group):
    meta = {'allow_inheritance': True, 'auto_create_index': False}

    commander: User = ReferenceField(User)


if __name__ == '__main__':
    from settings import load_settings
    from APIs.TalpiotSystem import Vault

    load_settings()
    # Vault.get_vault().connect_to_db()

    print(Group.objects[0].participants)

