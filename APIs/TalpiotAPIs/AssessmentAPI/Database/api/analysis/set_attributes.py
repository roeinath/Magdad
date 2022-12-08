from APIs.TalpiotAPIs.AssessmentAPI.Database import *
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.pipeline import PipeLine

_db_objects = [] # [Affiliation, Course, PlatformGrade, Platform, Talpion, Team,
             #  Division, Machzor]


class SetAttr(PipeLine):

    def __init__(self, attribute, value):
        PipeLine.__init__(self,
                          lambda prev: SetAttr.set_attribute(prev, attribute,
                                                             value))

    @staticmethod
    def set_attribute(prev, attr, value):
        def do_set(elem):
            if attr in vars(elem) and type(getattr(elem, attr)) is not type(
                value):
                raise Exception(f"Set type doesn't match! "
                                f"Should be {type(getattr(elem, attr))} but"
                                f" got {type(value)}")
            setattr(elem, attr, value)
            elem.save()
            return elem

        return list(map(do_set, prev))


mongo_vars = ["MultipleObjectsReturned", "DoesNotExist", "objects"]


def generate_setters():
    ret_str = "# " + "-" * 20 + " AUTO GENERATED " + "-" * 20 + "\n"
    ret_str += "class Setters:\n"
    for obj in _db_objects:
        vrs = vars(obj)
        for variable in vrs:
            if variable[0] == "_" or variable in mongo_vars or callable(getattr(obj, variable)):
                continue
            ret_str += f"    {obj.__name__}_{variable} =" \
                       f" lambda value: SetAttr('{variable}', value)\n"
        ret_str += "\n"
    return ret_str + "# " + "-" * 20 + " AUTO GENERATED " + "-" * 20


# -------------------- AUTO GENERATED --------------------
class Setters:
    Affiliation_name = lambda value: SetAttr('name', value)
    Affiliation_talpions = lambda value: SetAttr('talpions', value)
    Affiliation_id = lambda value: SetAttr('id', value)

    Course_name = lambda value: SetAttr('name', value)
    Course_id_number = lambda value: SetAttr('id_number', value)
    Course_credits = lambda value: SetAttr('credits', value)
    Course_field = lambda value: SetAttr('field', value)
    Course_course_grades = lambda value: SetAttr('course_grades', value)
    Course_id = lambda value: SetAttr('id', value)

    PlatformGrade_platform = lambda value: SetAttr('platform', value)
    PlatformGrade_talpion_id = lambda value: SetAttr('talpion_id', value)
    PlatformGrade_grades = lambda value: SetAttr('grades', value)
    PlatformGrade_grade_xml = lambda value: SetAttr('grade_xml', value)
    PlatformGrade_semester = lambda value: SetAttr('semester', value)
    PlatformGrade_commander_summary = lambda value: SetAttr('commander_summary', value)
    PlatformGrade_talpion = lambda value: SetAttr('talpion', value)
    PlatformGrade_id = lambda value: SetAttr('id', value)

    Platform_name = lambda value: SetAttr('name', value)
    Platform_platform_grades = lambda value: SetAttr('platform_grades', value)
    Platform_id = lambda value: SetAttr('id', value)

    Talpion_name = lambda value: SetAttr('name', value)
    Talpion_gender = lambda value: SetAttr('gender', value)
    Talpion_id_number = lambda value: SetAttr('id_number', value)
    Talpion_personal_number = lambda value: SetAttr('personal_number', value)
    Talpion_course_grades = lambda value: SetAttr('course_grades', value)
    Talpion_platform_grades = lambda value: SetAttr('platform_grades', value)
    Talpion_affiliations = lambda value: SetAttr('affiliations', value)
    Talpion_team = lambda value: SetAttr('team', value)
    Talpion_division = lambda value: SetAttr('division', value)
    Talpion_machzor = lambda value: SetAttr('machzor', value)
    Talpion_id = lambda value: SetAttr('id', value)

    Team_commander = lambda value: SetAttr('commander', value)

    Division_commander = lambda value: SetAttr('commander', value)
    Division_teams = lambda value: SetAttr('teams', value)

    Machzor_number = lambda value: SetAttr('number', value)
    Machzor_commander = lambda value: SetAttr('commander', value)
    Machzor_divisions = lambda value: SetAttr('divisions', value)

# -------------------- AUTO GENERATED --------------------


if __name__ == "__main__":
    print(generate_setters())
