import sys

from APIs.TalpiotAPIs.AssessmentAPI.Database.course import Course
from APIs.TalpiotAPIs.AssessmentAPI.Database.course_grade import CourseGrade
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.uploaddata.ExcelParser import ExcelParser
from APIs.TalpiotSystem import TalpiotSettings, TalpiotDatabaseCredentials, Vault
from APIs.TalpiotAPIs import db_helper
import tqdm


class UserNotFoundException(Exception):
    pass


def course_already_exists(course_id, is_real_data=False):
    return len(Course.objects.filter(id_number=course_id, is_real_data=is_real_data)) > 0


def course_grade_already_exists(course, user, is_real_data=False):
    return len(CourseGrade.objects.filter(course=course, user=user, is_real_data=is_real_data)) > 0


def upload_courses(students_data, mahzor, is_real_data=False, update=False):
    """
    function for upload courses from madar format
    :param students_data:
    :param mahzor:
    :param is_real_data:
    :param update: True iff want to update exist courses
    :return:
    """
    for row in tqdm.tqdm(students_data):
        course_name = row.get('שם הקורס')
        course_huji_id = row.get('מספר הקורס')
        year = row.get('שנה')
        credits = row.get('נקודות זכות')
        field = row.get('פקולטה')

        course = Course(name=course_name, id_number=course_huji_id, credits=credits, field=field,
                        is_real_data=is_real_data)

        if not course_already_exists(course_huji_id, is_real_data=is_real_data):
            course.save()
        else:
            course = Course.objects.filter(id_number=course_huji_id, is_real_data=is_real_data).first()

        user_name = row.get('שם התלמיד')

        ### this case is only for uploading data with the madar ###
        problematic_user_name = ["יוגב מוזס", "רם גולדשטיין"]
        new_user_name = ["יוגב  מוזס", "רם גולדשטין"]
        if user_name not in problematic_user_name:
            continue

        for i, name in enumerate(problematic_user_name):
            if user_name == name:
                user_name = new_user_name[i]
                break
        ### end specific case with madar ###

        user = User.objects.filter(name=user_name, mahzor=mahzor).first()
        if user is None:
            print(f'user {user_name} not found, can\'t upload {course_name}')
            continue

        # the case we are not updating need to check if already exist in DB
        if not update:
            if course_grade_already_exists(course, user, is_real_data=is_real_data):
                print(f'course {course_name} exist for {user_name}, not uploading')
                continue

        grade = row.get('ציון סופי')
        grade = CourseGrade.encrypt(grade)

        if not course_grade_already_exists(course, user, is_real_data=is_real_data):
            course_grade = CourseGrade(course=course, user=user, grade=grade, year=year, is_real_data=is_real_data)
            course_grade.save()
        else:
            # the case newer data is given - so need to update
            exist_course_grade = CourseGrade.objects.filter(course=course, user=user, is_real_data=is_real_data).first()
            exist_course_grade.grade = grade
            exist_course_grade.save()


if __name__ == '__main__':
    from APIs.init_APIs import main as set_up_DB
    set_up_DB()

    parser = ExcelParser('C:\\Users\\t9028387\\Downloads\\Mahzor_summary (1).xlsx')
    students_data = parser.get_data_from_sheet(0)
    upload_courses(students_data, 43, is_real_data=False, update=False)

    # print([u.name for u in User.objects.filter(mahzor=43)])
