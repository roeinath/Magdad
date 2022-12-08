from APIs.TalpiotAPIs.AssessmentAPI.Database.api.pipeline import PipeLine
from APIs.TalpiotAPIs.AssessmentAPI.Database.platform_grade import PlatformGrade
# from APIs.TalpiotAPIs.AssessmentAPI.Database.platform import Platform

# _db_objects = [PlatformGrade, Platform]


class GetAttr(PipeLine):
    SECRET = "__internal_parent"

    def __init__(self, attribute):
        PipeLine.__init__(self,
                          lambda prev: GetAttr.get_attribute(prev, attribute))

    @staticmethod
    def get_attribute(prev, attr):

        def execute_getter(elem):
            if GetAttr.SECRET in elem:
                elem[attr] = getattr(elem[GetAttr.SECRET], attr)
                return elem
            else:
                return {GetAttr.SECRET: elem, attr: getattr(elem, attr)}

        return map(execute_getter, prev)


mongo_vars = ["MultipleObjectsReturned", "DoesNotExist", "objects"]


def generate_getters():
    ret_str = "# " + "-" * 20 + " AUTO GENERATED " + "-" * 20 + "\n"
    ret_str += "class Getters:\n"
    for obj in _db_objects:
        vrs = vars(obj)
        for variable in vrs:
            if variable[0] == "_" or variable in mongo_vars or callable(getattr(obj, variable)):
                continue
            ret_str += f"    {obj.__name__}_{variable} = " \
                       f"GetAttr('{variable}')\n"
        ret_str += "\n"
    return ret_str + "# " + "-" * 20 + " AUTO GENERATED " + "-" * 20


class Getters:
    Affiliation_name = GetAttr('name')
    Affiliation_talpions = GetAttr('talpions')
    Affiliation_id = GetAttr('id')

    Course_name = GetAttr('name')
    Course_id_number = GetAttr('id_number')
    Course_credits = GetAttr('credits')
    Course_field = GetAttr('field')
    Course_course_grades = GetAttr('course_grades')
    Course_id = GetAttr('id')

    PlatformGrade_platform = GetAttr('platform')
    PlatformGrade_talpion_id = GetAttr('talpion_id')
    PlatformGrade_grades = GetAttr('grades')
    PlatformGrade_grade_xml = GetAttr('grade_xml')
    PlatformGrade_semester = GetAttr('semester')
    PlatformGrade_commander_summary = GetAttr('commander_summary')
    PlatformGrade_talpion = GetAttr('talpion')
    PlatformGrade_id = GetAttr('id')

    Platform_name = GetAttr('name')
    Platform_platform_grades = GetAttr('platform_grades')
    Platform_id = GetAttr('id')

    Talpion_name = GetAttr('name')
    Talpion_gender = GetAttr('gender')
    Talpion_id_number = GetAttr('id_number')
    Talpion_personal_number = GetAttr('personal_number')
    Talpion_course_grades = GetAttr('course_grades')
    Talpion_platform_grades = GetAttr('platform_grades')
    Talpion_affiliations = GetAttr('affiliations')
    Talpion_team = GetAttr('team')
    Talpion_division = GetAttr('division')
    Talpion_machzor = GetAttr('machzor')
    Talpion_id = GetAttr('id')

    Team_commander = GetAttr('commander')

    Division_commander = GetAttr('commander')
    Division_teams = GetAttr('teams')

    Machzor_number = GetAttr('number')
    Machzor_commander = GetAttr('commander')
    Machzor_divisions = GetAttr('divisions')


# -------------------- AUTO GENERATED --------------------


if __name__ == "__main__":
    print(generate_getters())
