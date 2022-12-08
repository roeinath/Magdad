from __future__ import annotations
from mongoengine import ReferenceField

from APIs.TalpiotAPIs.Group.commanded_group import CommandedGroup
from APIs.TalpiotAPIs.Group.mahzor_group import MahzorGroup


class DivisionGroup(CommandedGroup):
    mahzor : MahzorGroup = ReferenceField(MahzorGroup)


if __name__ == '__main__':
    from settings import load_settings
    from APIs.TalpiotSystem import Vault

    load_settings()
    # Vault.get_vault().connect_to_db()

    print(list(DivisionGroup.objects)[-1].participants)

