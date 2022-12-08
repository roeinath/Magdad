import datetime

from mongoengine import *


class Classroom(Document):
    meta = {'collection': 'classroom'}

    name: str = StringField(required=True)
    short_name: str = StringField(required=True)
    authorized_roles: [str] = ListField()
    allowed_start_time: dict = DictField(required=False)  # EXAMPLE {"hours": 19, "minutes": 00}

    def get_name(self) -> str:
        """
        Returns the name of the Classroom object.

        :return: String
        """
        return self.name
