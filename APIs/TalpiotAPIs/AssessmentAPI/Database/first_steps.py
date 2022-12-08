from APIs.TalpiotAPIs.AssessmentAPI.Database.platform import Platform
from APIs.TalpiotSystem import TalpiotSettings, TalpiotDatabaseCredentials, Vault
from APIs.TalpiotAPIs.AssessmentAPI.Database.platform_grade import PlatformGrade
from APIs.TalpiotAPIs.User.user import User


def experiment():
    new = Platform(name="elements")
    new.save()


"""
 platform = ReferenceField('Platform', required=True)
    user = ReferenceField('User', required=True)
    grades = MapField(FloatField(), default={})
    worded_grades = MapField(StringField(), default={})
    grade_xml = StringField(default="")
    year = IntField(min_value=1979, max_value=3000, required=True)
    semester = StringField(validation=_validate_sem, required=True)
    week = IntField(min_value=0, max_value=20, default=0)
    commander_summary = StringField(default="")
"""


def get_by_name_user(name):
    return User.objects.filter(name=name).first()


def get_by_name_platform(name):
    return Platform.objects.filter(name=name).first()


def platform_grade_object():
    first_plaform_grade = PlatformGrade(platform=get_by_name_platform("elements"), user=get_by_name_user("רום פייביש"),
                                        grades={'grade1': 100.0},
                                        worded_grades={'positive': 'we good'}, year=2021, semester='A', week=10,
                                        commander_summary='sucsses')
    first_plaform_grade.save()


if __name__ == '__main__':
    from APIs.init_APIs import main as set_up_DB
    set_up_DB()

    experiment()
    platform_grade_object()
    platform_grade_object()
