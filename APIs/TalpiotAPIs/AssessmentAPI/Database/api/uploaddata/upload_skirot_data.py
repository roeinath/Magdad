"""
Code for saving data from Excel file created by find_skirot_data.py to the Talpix DB
"""
from APIs.TalpiotAPIs.AssessmentAPI.Database.platform import Platform
from APIs.TalpiotAPIs.AssessmentAPI.Database.platform_grade import PlatformGrade
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotSystem import TalpiotDatabaseCredentials, Vault
from APIs.settings import load_settings
import tqdm

from APIs.init_APIs import main as set_up_DB


def plat_already_exists(platform_name, is_real_data=False):
    """
    A function for checking if a given platform already exists in the db
    :param platform_name: the name of the platform to check
    :param is_real_data: need to separate platforms with real data
    :return: boolean
    """
    return len(Platform.objects.filter(name=platform_name, is_real_data=is_real_data)) > 0


def plat_grade_already_exists(platform, user, year, semester, is_real_data=False):
    """
    A function for checking if a given user already has a grade in a given platform
    :param platform_name: the name of the platform to check
    :param is_real_data: need to separate platforms with real data
    :param user: the user to check
    :return: boolean
    """
    return len(PlatformGrade.objects.filter(platform=platform, user=user, year=year, semester=semester,
                                            is_real_data=is_real_data)) > 0


def upload_platforms(user_name, data, platforms, mahzor, year, semester, is_real_data=False, update="n"):
    """
    A function for uploading Skira from year 1 to the DB
    :param parser: an Excel parser for the data file
    :param mahzor: the mahzor which the Skirot belong to
    :param is_real_data: separating real grades from the fake
    :param update: True if we want to update existing platform's grades
    """
    msg = ""
    index_on_platforms = -1
    platform_names = [p[0] for p in platforms]
    platform_types = [p[1] for p in platforms]

    user = User.objects.filter(name=user_name, mahzor=mahzor).first()

    if user is None:
        return False, f'הצוער {user_name} לא נמצא'

    for row in tqdm.tqdm(data):
        # Iterate on all platform of a given cadet
        index_on_platforms += 1
        platform_name = platform_names[index_on_platforms]
        print(f"\n{platform_name} - {user_name}")

        if platform_name == "ממוצע מחזורי":
            continue

        platform = Platform(name=platform_name, type=platform_types[index_on_platforms], is_real_data=is_real_data)

        if not plat_already_exists(platform_name, is_real_data=is_real_data):
            platform.save()
        else:
            platform = Platform.objects.filter(name=platform_name, is_real_data=is_real_data).first()

        grades = {}
        try:
            for g in row:
                grades[g] = PlatformGrade.encrypt(float(row[g]))
        except:
            return False, f"ציוני הצוער {user_name} לא בפורמט הנכון"
        # The case we are not updating need to check if already exist in DB
        is_platform_grade_exist = plat_grade_already_exists(platform, user, year=year, semester=semester, is_real_data=is_real_data)
        if update == "n":
            if is_platform_grade_exist:
                return False, f'{platform_name} כבר קיים עבור {user_name}. התכוונת למצב עדכון?'
            plat_grade = PlatformGrade(platform=platform, user=user, grades=grades, worded_grades={}, year=year,
                                       semester=semester, is_real_data=is_real_data)
            plat_grade.save()

        if update == "y":
            # Update mode, update the old data with the new one
            if is_platform_grade_exist:
                exist_course_grade = PlatformGrade.objects.filter(platform=platform, user=user, year=year, semester=semester,
                                             is_real_data=is_real_data).first()
                exist_course_grade.grades = grades
                exist_course_grade.save()

            else:
                plat_grade = PlatformGrade(platform=platform, user=user, grades=grades, worded_grades={}, year=year,
                                           semester=semester, is_real_data=is_real_data)
                plat_grade.save()
                msg = f' ציוני {platform_name} עודכנו עבור {user_name}'

    return True, msg
