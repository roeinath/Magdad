from enum import Enum

from mongoengine import Document, ReferenceField, EnumField, DateField

from APIs.TalpiotAPIs import User


class TarganStatus(Enum):
    UNCHECKED = 0
    UNSIGNED = 1
    SIGNED = 2


class Responsible(Enum):
    A_MISHMAAT = 0
    DIVISION_COMMANDER = 1


class Targan(Document):
    user: User = ReferenceField('User')
    status: TarganStatus = EnumField(TarganStatus)
    date_given = DateField()
    date_signed_by_a_mishmaat = DateField()
    date_signed_by_division_commander = DateField()

    @staticmethod
    def get_all_targans_per_user(user: User):
        return Targan.objects(user=user)

    @staticmethod
    def get_all_users_with_unchecked_targans():
        return list(set([targan.user for targan in Targan.objects(status=TarganStatus.UNCHECKED)]))
