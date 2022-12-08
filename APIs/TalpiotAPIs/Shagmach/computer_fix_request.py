from datetime import datetime
from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField
from mongoengine.fields import BooleanField, IntField
from typing import List

from APIs.TalpiotAPIs.User.user import User


class FixTypes:
    BROKEN_SCREEN = 'מסך שבור'
    NO_INTERNET = 'חיבור אינטרנט תקול'
    RAMKOL_FIX = 'בעיות ברמקול'
    MICROPHONE_FIX = 'בעיות במיקרופון'
    RANDOM_SHUTDOWN = 'כיבוי אקראי'
    BATTERY_FIX = 'בעיות בסוללה'
    OTHER = 'אחר'

    @staticmethod
    def get_list():
        return [FixTypes.BROKEN_SCREEN, FixTypes.NO_INTERNET, FixTypes.RAMKOL_FIX, FixTypes.MICROPHONE_FIX,
                FixTypes.RANDOM_SHUTDOWN, FixTypes.BATTERY_FIX, FixTypes.OTHER]


class ComputerFixRequest(Document):
    name: str = StringField(required=False)
    user: str = ReferenceField(User, required=False)
    computer_id: str = StringField()
    phone_number: str = StringField(required=False)
    fix_type: str = StringField()
    description: str = StringField()
    is_computer_in_tamam: str = StringField()
    is_computer_working: str = StringField()
    computer_serial: str = StringField()
    finish_deadline: datetime = DateField()
    statuses: str = ListField(required=False)
    closed: bool = BooleanField()

    @staticmethod
    def new_request(name: str, computer_id: str, phone_number: str, fix_type: FixTypes, description: str,
                    is_computer_in_tamam: bool):
        return ComputerFixRequest(name=name, computer_id=computer_id, phone_number=phone_number, fix_type=fix_type,
                                  description=description, is_computer_in_tamam=is_computer_in_tamam)


class ComputerFixRequest2(Document):
    user: User = ReferenceField(User)
    time: datetime = DateTimeField()
    computer_id: str = StringField()
    fix_type: str = StringField()
    description: str = StringField()
    is_computer_in_tamam: str = StringField()
    is_computer_working: str = StringField()
    computer_serial: str = StringField()
    finish_deadline: datetime = DateField()
    statuses: str = ListField()
    closed: bool = BooleanField(default=False)

    @staticmethod
    def new_request(computer_id: str, fix_type: FixTypes, description: str, is_computer_in_tamam: bool):
        return ComputerFixRequest2(computer_id=computer_id, fix_type=fix_type, description=description,
                                   is_computer_in_tamam=is_computer_in_tamam)
