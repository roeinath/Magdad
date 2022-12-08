from __future__ import annotations

from typing import List

from mongoengine import Document, ListField, ReferenceField, BinaryField

from APIs.TalpiotAPIs.Group.group import Group
from APIs.TalpiotAPIs.Group.mahzor_group import MahzorGroup
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotSystem import Vault
from APIs.settings import load_settings


#############################################################
#    There should always be only 1 StaticFields Document    #
#############################################################

class StaticFields(Document):
    meta = {'collection': 'static_fields', 'allow_inheritance': True, 'auto_create_index': False}

    current_mahzors: List[MahzorGroup] = ListField(ReferenceField(MahzorGroup))
    current_sagab_group: Group = ReferenceField(Group)
    google_drive_token: bytes = BinaryField()
    db_collections: list = ListField()

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        # raise Exception("StaticFields documents should never be created, the sole object should be updated instead")

    def __repr__(self):
        return self.name

    def __contains__(self, user: User) -> bool:
        """
        This method checks if a user is in a certain group.
        Usage: if my_user in group: do something
        Args:
            user: the user object to check

        Returns: true iff the user is in the group.

        """
        return user in self.participants


def get_static_fields():
    return StaticFields.objects()[0]


def get_mahzor_number_list() -> List[int]:
    current_mahzors: List[MahzorGroup] = get_static_fields().current_mahzors
    return [mahzor.mahzor_num for mahzor in current_mahzors]


def create_static_fields_for_the_first_time():
    load_settings()
    Vault.get_vault().connect_to_db()
    sf = StaticFields(current_mahzors=[], current_sagab_group=None)
    sf.save()


def get_db_collections():
    vault = Vault.get_vault()
    static_fields: StaticFields = get_static_fields()
    return static_fields.db_collections


def update_db_collections():
    vault = Vault.get_vault()
    static_fields: StaticFields = vault.objects_from_main_db(StaticFields)[0]
    static_fields.db_collections = vault.list_collection_names()
    static_fields.save()
    return static_fields.db_collections
