from APIs.TalpiotAPIs.AssessmentAPI.Database.platform import Platform
from APIs.TalpiotSystem import TalpiotSettings, TalpiotDatabaseCredentials, Vault
from APIs.TalpiotAPIs.AssessmentAPI.Database.platform_grade import PlatformGrade
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.querycalls.filter import Filter
from APIs.TalpiotAPIs.AssessmentAPI.Database.course_grade import CourseGrade
from APIs.TalpiotAPIs.AssessmentAPI.Database.course import Course
from APIs.TalpiotAPIs.Group.group import Group
from web_features.personal_page.permissions import *
from APIs.TalpiotAPIs.Group.mahzor_group import MahzorGroup
from APIs.TalpiotAPIs.Group.division_group import DivisionGroup
from APIs.init_APIs import main as connect_db

import csv
import random

"""
functions:

get_by_name_group
get_courses_of_user
get_single_course_of_group
get_courses_of_group
get_courses_list_for_group
get_grade_from_coursegrade
get_divisions_of_mahzor
get_color_for_cadets_by_division
"""


def get_by_name_group(name):
    return Group.objects.filter(name=name).first().select_related(1)


def get_courses_of_user(name, year, is_real_data=False, field='all'):
    """
    getting cadet's course grades and his average
    :param name: str
    :param year: int
    :param is_real_data: bool
    :param field: math , psychics or CS
    :return: array of the cadet's grades and his average
    """
    user = get_user_by_name(name)
    if year == "all":
        course_grades = list(CourseGrade.objects.filter(user=user, is_real_data=True).select_related(2))
    else:
        course_grades = list(CourseGrade.objects.filter(user=user, is_real_data=True, year=year).select_related(2))

    temp_avg_grades = 0
    sum_of_credits = 0
    grades = {}
    if field == 'all':
        for course_grade in course_grades:
            if course_grade.course.credits > 0:
                data = get_grade_from_coursegrade(course_grade, is_real_data)
                moed_a_data = CourseGrade.decrypt(course_grade.moed_a_grade) if course_grade.moed_a_grade is not None \
                    else None

                grades[course_grade.course.name] = {"semester": course_grade.semester, "grade": data,
                                                    "credits": course_grade.course.credits,
                                                    "moed": course_grade.moed, "moed_a_grade": moed_a_data}

                # if not ptor add to the average
                if data != -1:
                    temp_avg_grades += data * course_grade.course.credits
                    sum_of_credits += course_grade.course.credits
    else:
        for course_grade in course_grades:
            if course_grade.course.field == field:
                if course_grade.course.credits > 0:
                    data = get_grade_from_coursegrade(course_grade, is_real_data)
                    moed_a_data = CourseGrade.decrypt(
                        course_grade.moed_a_grade) if course_grade.moed_a_grade is not None \
                        else None
                    if course_grade.year == year and (sum((1 for k in course_grades if course_grade.course.name ==
                                                                                       k.course.name)) == 1 or
                                                      year == mahzor_number_to_years[user.mahzor][0]):
                        grades[course_grade.course.name] = {"semester": course_grade.semester, "grade": data,
                                                            "credits": course_grade.course.credits,
                                                            "moed": course_grade.moed, "moed_a_grade": moed_a_data}
                        temp_avg_grades += data * course_grade.course.credits
                        sum_of_credits += course_grade.course.credits
    try:
        average = temp_avg_grades / sum_of_credits
    except ZeroDivisionError:
        average = -1

    return grades, average


def get_single_course_of_group(group_name, year, is_real_data, course_name):
    group = get_by_name_group(group_name)
    course_grades = CourseGrade.objects.filter(user__in=group.participants, year=year,
                                               is_real_data=True).select_related(1)
    grade_array = [0]
    for course_grade in course_grades:
        if course_grade.course.name == course_name:
            grade_array[0] += 1
            grade_array.append(
                (course_grade.user.name, get_grade_from_coursegrade(course_grade, is_real_data)))
    return grade_array


def get_single_course_of_group(group_name, year, is_real_data, course_name):
    group = get_by_name_group(group_name)
    course_grades = CourseGrade.objects.filter(user__in=group.participants, year=year,
                                               is_real_data=True).select_related(1)
    grade_array = [0]
    for course_grade in course_grades:
        if course_grade.course.name == course_name:
            grade_array[0] += 1
            grade_array.append(
                (course_grade.user.name, get_grade_from_coursegrade(course_grade, is_real_data)))
    return grade_array


def get_courses_of_group(group_name, year, is_real_data, threshold=1):
    """
    getting the courses of the group with their grades
    :param group_name: the name of the group (string)
    :param year: the year (int)
    :param is_real_data: bool
    :return: dictionary with keys of relevant courses of group, and values
    as arrays, the first val in the array is the number of the cadets did the course
    and the other values are tuples with the name of the cadet and his grade in the course
    """

    group = get_by_name_group(group_name)
    course_grades = CourseGrade.objects.filter(user__in=group.participants, year=year,
                                               is_real_data=True).select_related(1)
    group_courses = {}

    for course_grade in course_grades:
        if course_grade.course.credits > 0:
            if course_grade.course.name not in group_courses:
                group_courses[course_grade.course.name] = [1, (
                    course_grade.user.name, get_grade_from_coursegrade(course_grade, is_real_data))]
            else:
                group_courses[course_grade.course.name][0] += 1
                group_courses[course_grade.course.name].append(
                    (course_grade.user.name, get_grade_from_coursegrade(course_grade, is_real_data)))

    real_group_courses = {}
    for course in group_courses:
        if group_courses[course][0] >= threshold:
            real_group_courses[course] = group_courses[course]

    return real_group_courses


def get_courses_list_for_group(group_name, year):
    """
    :return: list with strings of the courses a group has
    """
    group = get_by_name_group(group_name)
    course_grades = CourseGrade.objects.filter(user__in=group.participants, year=year,
                                               is_real_data=True).select_related(1)
    names = set()
    for course_grade in course_grades:
        if course_grade.course.name not in names and course_grade.course.credits > 0:
            names.add(course_grade.course.name)
    return list(names)


def get_grade_from_coursegrade(course_grade: CourseGrade, is_real_data):
    """
    return real data of given course grade or randint
    :param course_grade: CourseGrade object
    :param is_real_data: bool
    :return: float
    """
    if is_real_data:
        return CourseGrade.decrypt(course_grade.grade)
    else:
        return random.randint(0, 100)


def get_divisions_of_mahzor(mahzor_num):
    """
    get all the divisions in mahzor
    :param mahzor_num: the number of the mahzor
    :return: list of the divisions groups objects
    """
    mahzor_filter = Filter.is_filter("mahzor_num", mahzor_num)
    get_divisions_filter = Filter.matches_query("mahzor", mahzor_filter, MahzorGroup)
    divisions = get_divisions_filter.execute(DivisionGroup)

    return divisions


def get_color_for_cadets_by_division(mahzor_num, names):
    """
    get the color of cadets by division
    :param mahzor_num:
    :param names:
    :return: list of colors, cadets_colors_lst[i] is for name[i] (by division)
    """
    colors_list = ["#ffdac1", "#b5ead7", "#c7ceea", "#ffffff"]
    cadets_colors_lst = []
    divisions = get_divisions_of_mahzor(mahzor_num)
    divisions_index = {division.name: i for i, division in enumerate(divisions)}

    # dictionary for matching a color to division
    divisions_colors_dict = {}
    # list for the names in each division
    divisions_names = [0 for i in range(len(divisions))]
    for division in divisions:
        index = divisions_index[division.name]
        divisions_names[index] = [user.name for user in division.participants]
        divisions_colors_dict[division.name] = colors_list[index]
    for name in names:
        if len(divisions_names) == 0:  # If there is no division (Sagaz has no divisions as to 2022)
            cadets_colors_lst.append(colors_list[-1])
            continue

        for i, division in enumerate(divisions_names):
            if name in division:
                cadets_colors_lst.append(colors_list[i])
                break

            # the case of name missing in group
            if i == len(divisions_names) - 1:
                print(f"missing {name} in  mahzor {mahzor_num} divisions")
                cadets_colors_lst.append(colors_list[-1])

    colors_dict_by_division = {"cadets_colors_lst": cadets_colors_lst, "divisions_colors_dict": divisions_colors_dict}
    return colors_dict_by_division


def return_relevant_exgrade(course_grade: CourseGrade, is_real_data):
    """
    return real data of given course exercise grade or randint
    :param course_exgrade: CourseGrade object
    :param is_real_data: bool
    :return: dict of exersice and grade
    """
    if is_real_data:
        pass
        return {}
        # return CourseGrade.decrypt(course_grade.grade)
    else:
        num_exersices = random.randint(0, 4)
        dict_exe = {}
        for x in range(num_exersices):
            dict_exe[x] = random.randint(0, 100)
        return dict_exe


def get_exgrades_of_user(name, year, is_real_data=False, field='all'):
    '''
    getting caset's exercise grades
    :param name: string
    :param year: int
    :param is_real_data:bool
    :param field:  math , psychics or CS
    :return:
    '''
    user = User.objects(name=name).first()
    course_grades = list(CourseGrade.objects.filter(user=user, year=year, is_real_data=True).select_related(2))
    grades = []
    if field == 'all':
        for course_grade in course_grades:
            if course_grade.course.credits > 0:
                data_dict = return_relevant_exgrade(course_grade, is_real_data)
                for value in data_dict:
                    grades.append((course_grade.user.name, course_grade.course.name, value, data_dict[value]))
    return grades


def get_name_course_by_number(grades):
    '''
    for each course in dict returns the name of course if exists in DB
    :param grades: dict of {course_num: grades}
    :return: dict of {course_num: course_name}
    '''
    course_objects = Course.objects.filter().select_related(1)
    course_names = {}
    for course_num in grades:  # creates dict {course_num : None}
        course_names[str(course_num)] = None
    for c in course_objects:
        if str(c.id_number) in course_names:
            course_names[str(c.id_number)] = c.name
    return course_names


def delete_duplicates(relevant_years=[2016, 2017, 2018, 2019, 2020, 2021, 2022]):
    usr_courses_dict = {}
    course_grades = list(CourseGrade.objects.filter(is_real_data=True,
                                                    year__in=relevant_years).select_related(
        2))
    for grade in course_grades:
        if grade.user.name in usr_courses_dict:
            if grade.course.id_number in usr_courses_dict[grade.user.name].keys():
                if grade.semester is None:
                    grade.delete()
                    print(f"delete {grade}, grade is None")
                else:
                    print(f"delete {usr_courses_dict[grade.user.name][grade.course.id_number]}, grade is not None")
                    usr_courses_dict[grade.user.name][grade.course.id_number].delete()
                    usr_courses_dict[grade.user.name][grade.course.id_number] = grade
            else:
                usr_courses_dict[grade.user.name][grade.course.id_number] = grade
        else:
            usr_courses_dict[grade.user.name] = {}
            usr_courses_dict[grade.user.name][grade.course.id_number] = grade


if __name__ == "__main__":
    # import time

    connect_db()
    delete_duplicates()
    # start = time.time()
    # user = "אלון קגן"
    # print(get_courses_of_user(user, 2021, is_real_data=True))
    # end = time.time()
    # print("Finished", end - start)
