from APIs.TalpiotAPIs.AssessmentAPI.Database.platform import Platform
from APIs.TalpiotSystem import TalpiotSettings, TalpiotDatabaseCredentials, Vault
from APIs.TalpiotAPIs.AssessmentAPI.Database.platform_grade import PlatformGrade
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.querycalls.filter import Filter
from APIs.TalpiotAPIs.AssessmentAPI.Database.course_grade import CourseGrade
from APIs.TalpiotAPIs.AssessmentAPI.Database.course import Course
from APIs.TalpiotAPIs.Group.group import Group
from APIs.TalpiotAPIs.Group.team_group import TeamGroup
from web_framework.server_side.infastructure.constants import *
from APIs.init_APIs import main as connect_db
from APIs.TalpiotSystem import TalpiotSettings

import csv
import random

"""
code for skirot data

functions:
get_by_name_group
get_major_platforms_of_group
get_skira_of_user
get_grades_of_user
get_by_name_group
get_grade_of_platformgrade

get_skirot_of_group
get_team_of_sagaz
get_user_by_name
"""


def set_up_DB():
    connect_db()


def get_by_name_group(name):
    return Group.objects.filter(name=name).first()


def get_major_platforms_of_group(group: Group,year,sem):
    """

    :param group:  The group we want to pull from
    :return: the platforms of the groups
    """
    platform_grades = list(PlatformGrade.objects.filter(user__in=group.participants,year = year,
                                                        semester =sem).select_related(1))
    platform_options = {}
    counter_dict = {}
    for pg in platform_grades:
        if pg.platform not in counter_dict.keys():
            counter_dict[pg.platform] = 0
        counter_dict[pg.platform] += 1
    for p, i in counter_dict.items():
        if i >= 3:
            platform_options[str(p.id)] = p.name
    return platform_grades, platform_options, counter_dict


def get_skira_of_user(name, is_real_data=False):
    """
    getting cadet's course grades and his average
    :param name: string
    :param is_real_data: bool
    :return:
    """
    user = User.objects(name=name).first()
    platform_grades = list(PlatformGrade.objects.filter(user=user, is_real_data=is_real_data).select_related(2))
    #print("Plat Grades of {}:\n".format(name),platform_grades)
    grades_dict = {}
    for platform_grade in platform_grades:
        info = {"year": platform_grade.year, "semester": platform_grade.semester}
        grades_dict[(platform_grade.platform.name, platform_grade.year, platform_grade.semester)] = {
            "grades": platform_grade.decrypted_grades(is_real_data=is_real_data),
            "info": info}

    return grades_dict


def get_grades_of_user(name, is_real=False):
    """
    :param is_real: if is_real get the real information
    :param name: user name as seen as User class
    :return: the users grades
    """
    if not is_real:
        return {"check": {"grades": {"aa": 0, "b": 1, "c": 3}, "info": {"year": 2021, "semester": "B"}},
                "check2": {"grades": {"aa": 2, "b": 6, "c": 2}, "info": {"year": 2021, "semester": "A"}},
                "check3": {"grades": {"aa": 3, "b": 5, "c": 3}, "info": {"year": 2021, "semester": "B"}},
                "check4": {"grades": {"aa": 4, "b": 6, "c": 4}, "info": {"year": 2021, "semester": "B"}}}

    all_grades_filter = \
        Filter.matches_query("user", Filter.is_filter("name", name), User)
    platform_grades = all_grades_filter.execute(PlatformGrade)

    grades_dict = {}
    for platform_grade in platform_grades:
        info = {"year": platform_grade.year, "semester": platform_grade.semester}
        grades_dict[platform_grade.platform.name] = {"grades": platform_grade.decrypted_grades, "info": info}

    return grades_dict


def get_by_name_group(name):
    """
    :return: group object related to a given name
    """
    return Group.objects.filter(name=name).first()


def get_grade_of_platformgrade(platform_grade: PlatformGrade, is_real_data):
    """
    return real data of given platform grade or randint
    :param platform_grade: PlatformGrade object
    :param is_real_data: bool
    :return: float
    """
    if is_real_data:
        return CourseGrade.decrypt(platform_grade.grade)
    else:
        return random.randint(1, 6)


def get_skirot_of_group(group_name, is_real_data):
    """
    getting the courses of the group with their grades
    :param group_name: the name of the group (string)
    :param is_real_data: bool
    :return: dictionary with keys of relevant courses of group, and values
    as arrays, the first val in the array is the number of the cadets did the course
    and the other values are tuples with the name of the cadet and his grade in the course
    """

    group = get_by_name_group(group_name)
    skirot_grades = PlatformGrade.objects.filter(user__in=group.participants).select_related(1)
    group_platforms = {}

    for platform_grade in skirot_grades:
        if platform_grade.platform.name not in group_platforms:
            group_platforms[platform_grade.platform.name] = [1, (
                platform_grade.platform.name, get_grade_of_platformgrade
                (platform_grade, is_real_data))]
        else:
            group_platforms[platform_grade.platform.name][0] += 1
            group_platforms[platform_grade.platform.name].append(
                (platform_grade.platform.name, get_grade_of_platformgrade
                (platform_grade, is_real_data)))
    # print(group_platforms)
    return group_platforms


def get_team_of_sagaz(user):
    """
    get the team of the sagaz
    :param user:
    :return: list of users
    """
    team = TeamGroup.objects.filter(commander=user)
    if len(team) == 0:
        return []
    return team[0].participants


def get_user_by_name(name):
    return User.objects.filter(name=name).first()


NAME = "עידו עברי"

if __name__ == "__main__":
    set_up_DB()
    # print(get_user_by_name(NAME))
    #
    # set_up_DB()
    # name = "יואב פלטו"
    # yoav = get_user_by_name(name)
    # courses = PlatformGrade.objects.filter(user=yoav)
    # for platform in courses:
    #     print(platform)

    print(TalpiotSettings.is_master())
