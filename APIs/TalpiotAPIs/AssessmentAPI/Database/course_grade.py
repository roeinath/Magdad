from mongoengine import *
from cryptography.fernet import Fernet


def _validate_sem(sem):
    if sem not in ["A", "B", "A+B"]:
        raise ValidationError("Semester must be 'A' or 'B'")


def _validate_moed(moed):
    if moed not in ["A", "B"]:
        raise ValidationError("moed must be 'A' or  B")


class CourseGrade(Document):
    course = ReferenceField('Course', required=True)
    user = ReferenceField('User', required=True)
    grade = StringField()
    moed = StringField(validation=_validate_moed)
    year = IntField(required=True)
    semester = StringField(validation=_validate_sem)
    homework_grades = MapField(FloatField())
    moed_a_grade = StringField()
    is_real_data = BooleanField(default=False, required=True)  # boolean if the data is real or not

    meta = {'collection': 'course_grade'}

    __XOR_KEY = 1249
    __ACCURACY = 100.0
    __fernet_key = b'FVOwF-23paS9PIFBdmjCrYjhiQ6hyQEOfAcb832gS-0='

    @staticmethod
    def encrypt(val: float) -> str:
        val = str(val).encode()
        return Fernet(CourseGrade.__fernet_key).encrypt(val).decode()

    @staticmethod
    def decrypt(val: str) -> float:
        import time
        start = time.time()
        res = float(Fernet(CourseGrade.__fernet_key).decrypt(val.encode()).decode())
        end = time.time()
        # print("Time decrypt:", end - start )
        return res

    def __str__(self):
        return f"grade in \"{self.course}\" of {self.user} from {self.year}{self.semester}"


    class ExGrade(Document):
        course = ReferenceField('Course', required=True)
        user = ReferenceField('User', required=True)
        grade = StringField()
        year = IntField(required=True)
        semester = StringField(validation=_validate_sem)
        is_real_data = BooleanField(default=False, required=True)  # boolean if the data is real or not
