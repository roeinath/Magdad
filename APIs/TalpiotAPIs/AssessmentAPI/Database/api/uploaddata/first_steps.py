from APIs.TalpiotAPIs.AssessmentAPI.Database.platform import Platform
from APIs.TalpiotSystem import TalpiotSettings, TalpiotDatabaseCredentials, Vault
from APIs.TalpiotAPIs.AssessmentAPI.Database.platform_grade import PlatformGrade
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.uploaddata import params
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.querycalls.filter import Filter
import csv
import pandas as pd


def get_by_name_user(name):
    return User.objects.filter(name=name).first()


def get_by_name_platform(name):
    return Platform.objects.filter(name=name).first()


def get_all_users(mahzor):
    return [u.name for u in User.objects.filter(mahzor=mahzor)]


def create_dict(headers, csv_read):
    """
    creating the dictionary
    :param headers: list of titles
    :param csv_read: pointer to read the csv
    :return: dictionary of the csv data {title1: [data1, data2,...], title2: ...}
    """
    dict_csv = {}
    for row in csv_read:
        for counter in range(len(row)):
            if counter != 0:
                if headers[counter] in dict_csv.keys():
                    dict_csv[headers[counter]].append(row[counter])
                else:
                    dict_csv[headers[counter]] = [row[counter]]
    return dict_csv


def get_dict_csv():
    """
    getting the dict after creating it
    :return: dictionary of the csv data {title1: [data1, data2,...], title2: ...}
    """
    with open(params.CSV_PATH, encoding='utf8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        dict_csv = create_dict(header, csv_reader)
        return dict_csv


def create_single_platform_object(dict_csv, counter, platforma="מבואוצ", year=2021, semester="A", worded_grades={}):
    """
    creating one platform_grade object
    :param dict_csv:
    :param counter:
    :param platforma:
    :param year:
    :param semester:
    :param worded_grades:
    :return:
    """
    platform = platforma
    user = dict_csv["שם"][counter]
    print(get_by_name_user(user))
    year = year
    semester = semester
    worded_grades = worded_grades
    grades = {}
    for grade in dict_csv.keys():
        if grade != "שם":
            grades[grade] = dict_csv[grade][counter]

    new_platform_grade_object = PlatformGrade(platform=get_by_name_platform(platform), user=get_by_name_user(user),
                                              grades=grades,
                                              worded_grades=worded_grades, year=year, semester=semester, week=0,
                                              commander_summary='sucsses', is_real_data=True)

    if not is_exist_in_collection(new_platform_grade_object.platform.name, new_platform_grade_object.user.name):
        return new_platform_grade_object
    else:
        return None


def get_all_platform_objects():
    """
    uploading all the data from the file to a db
    :return: None
    """
    dict_csv = get_dict_csv()
    for counter in range(len(dict_csv['שם'])):
        PG_OBJECFT = create_single_platform_object(dict_csv, counter)
        if PG_OBJECFT is not None:
            print("save")
            PG_OBJECFT.save()

    return


def is_exist_in_collection(Platform, name):
    """

    :param Platform:
    :param name:
    :return:
    """
    plat_user = get_platfrom_and_user_in_collection(Platform, name)
    if len(plat_user) == 0:
        return False
    else:
        return True


def get_platfrom_and_user_in_collection(platform, name):
    """

    :param platform:
    :param name:
    :return:
    """
    get_plat_and_users = \
        Filter.matches_query("platform", Filter.is_filter("name", platform), Platform) + \
        Filter.matches_query("user", Filter.is_filter("name", name), User)
    plat_users = get_plat_and_users.execute(PlatformGrade)
    return plat_users


def get_grades_for_user_in_collection(platform, name):
    """

    :param platform:
    :param name:
    :return:
    """
    get_plat_and_users = \
        Filter.matches_query("platform", Filter.is_filter("name", platform), Platform) + \
        Filter.matches_query("user", Filter.is_filter("name", name), User)
    plat_users = get_plat_and_users.execute(PlatformGrade)
    grades = []

    for key in params.list_titles_grades:
        for g in plat_users:
            temp = PlatformGrade.decrypt(g.grades[key])
            grades.append(temp)
    return grades


if __name__ == "__main__":
    from APIs.init_APIs import main as set_up_DB
    set_up_DB()

    print(get_all_users(40))
    print(get_all_users(41))
    print(get_all_users(42))
    print(get_all_users(43))
