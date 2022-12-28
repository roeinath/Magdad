from __future__ import annotations
import datetime
from mongoengine import Document, EmailField, StringField, IntField, ReferenceField, LongField, BooleanField, ListField, DictField, DateField
from enum import Enum
from typing import List

from APIs.TalpiotAPIs.Role.role import Role
from APIs.TalpiotSystem import TBLogger

import time


class Gender(Enum):
    male = "male"
    female = "female"
    other = "other"


class User(Document):
    meta = {'collection': 'users_info'}

    email: str = EmailField(required=True)
    name: str = StringField(max_length=100)
    mahzor: int = IntField()
    gender: str = StringField(max_length=10)
    # todo use from typing import __future__
    team_commander: User = ReferenceField('self')
    mahzor_commander: User = ReferenceField('self')
    phone_number: str = StringField()
    telegram_id: int = LongField()
    mahzor_admin: bool = BooleanField()
    bot_admin: bool = BooleanField()
    special_attributes: dict = DictField()
    birthday: datetime.date = DateField()
    role: List[str] = ListField(StringField(), default=["מתלם"])  # TODO remove - left for legacy
    role_list: List[User] = ListField(ReferenceField(Role), required=False)  # TODO new roles field

    secret_code: str = StringField()
    user_attributes: List[dict] = ListField(DictField(), default=[{
            'identifier': 'שם מלא',
            'type': 'text_question',
            'category': 'מידע יבש',
            'question': 'שם מלא:',
            'required': False,
            'value': None}])

    @staticmethod
    def get_by_telegram_id(telegram_id: int):
        return User.objects.get(telegram_id=telegram_id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def __contains__(self, role: Role) -> bool:
        """
        This method checks if a role is in a certain user.
        Usage: if role in user: do something
        """
        # t0 = time.time()
        ans = role in self.role_list
        # t1 = time.time()
        # t += (t1-t0)
        # print(str(t) + " cont " + str(t1 - t0))
        return ans

    def has_role(self, role_name):
        """
        uses __containts__ but uses the role's name
        can process string and a list of strings
        """
        if type(role_name) == str:
            return Role.objects.get(name=role_name) in self

        if type(role_name) == property:
            TBLogger.warning('your Page or Category does not contain AUTH_ROLES list, hence will not be displayed')
            return False

        # t0 = time.time()
        roles = Role.objects.filter(name__in=role_name)
        # t1 = time.time()
        # print("    Quering from Role took " + str(t1 - t0))

        # t0 = time.time()
        ans = False
        for role in roles:
            if role in self:
                ans = True
                break

        # t1 = time.time()
        # print("    looking for User roles took " + str(t1 - t0))
        return ans

    def get_first_name(self) -> str:
        """
        Returns the first name of the user.

        :return:
        """
        return self.name.split(' ')[0]

    def get_last_name(self):
        """
        Returns the last name of the user.

        :return:
        """
        return self.name.split(' ')[-1]

    def get_short_name(self):
        """
        Returns first + last name of the user.

        :return:
        """

        return self.get_first_name() + " " + self.get_last_name()

    def get_full_name(self):
        if self.mahzor > 0:
            return f'{self.name} - {self.mahzor}'
        return self.name

    def get_gender(self):
        return Gender[self.gender]

    def get_team(self) -> List[User]:
        if self.team_commander is None:
            return []

        return User.objects(
            team_commander=self.team_commander,
            mahzor=self.mahzor
        )


    def update_special_attribute(self, key, value):
        """
        Updates the special attributes, in the specific
        key specified, And then updates the database.

        :param key: The key to update
        :param value: The new value
        :return:
        """

        self.special_attributes[key] = value
        self.save()

    def get_special_attribute(self, key):
        """
        Returns the special attribute with the given key.

        :param key: The key to retrieve
        :return:
        """
        try:
            return self.special_attributes[key]
        except KeyError:
            return None

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.id)




    
