
from mongoengine import *


class Classroom(Document):
    meta = {'collection': 'classroom'}

    name: str = StringField(required=True)
    short_name: str = StringField(required=True)
    authorized_roles: [str] = ListField()

    def get_name(self) -> str:
        """
        Returns the name of the Classroom object.

        :return: String
        """
        return self.name
