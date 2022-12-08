from cryptography.fernet import Fernet
from mongoengine import *

from APIs.TalpiotAPIs.AssessmentAPI.Database.course_grade import CourseGrade
from web_framework.server_side.infastructure.constants import *

import random


def generate_grades(key):
    if ARACHIM in key:
        return random.randint(1, 3)
    return random.randint(1, 6)


def _validate_sem(sem):
    if sem not in ["A", "B", "A+B"]:
        raise ValidationError("Semester must be 'A' or 'B'")


class PlatformGrade(Document):
    ___XOR_KEY = 1249
    __ACCURACY = 100.0
    __fernet_key = b'FVOwF-23paS9PIFBdmjCrYjhiQ6hyQEOfAcb832gS-0='

    platform = ReferenceField('Platform', required=True)
    user = ReferenceField('User', required=True)
    grades = MapField(StringField(), default={})
    worded_grades = MapField(StringField(), default={})
    # grade_xml = StringField(default="")
    year = IntField(min_value=1979, max_value=3000, required=True)
    semester = StringField(validation=_validate_sem, required=True)
    week = IntField(min_value=0, max_value=20, default=0)
    commander_summary = StringField(default="")
    is_real_data = BooleanField(default=False, required=True)  # boolean if the data is real or not

    meta = {'collection': 'platform_grade'}

    @property
    def talpion(self):
        return PlatformGrade.user  # check

    @staticmethod
    def encrypt(val: float) -> str:
        val = str(val).encode()
        return Fernet(PlatformGrade.__fernet_key).encrypt(val).decode()

    @staticmethod
    def decrypt(val: str) -> float:
        return float(Fernet(PlatformGrade.__fernet_key).decrypt(val.encode()).decode())

    def decrypted_grades(self, is_real_data=False):
        if is_real_data:
            return {key: self.decrypt(value) for key, value in self.grades.items()}
        return {key: generate_grades(key) for key, value in self.grades.items()}

    def __str__(self):
        return f"grade in \"{self.platform}\" of {self.talpion.name} from {self.year}{self.semester} week {self.week}"
