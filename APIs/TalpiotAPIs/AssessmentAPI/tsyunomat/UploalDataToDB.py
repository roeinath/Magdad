from web_features.Elements.personal_page.permissions import *


def course_already_exists(course_id, is_real_data=False):
    return len(Course.objects.filter(id_number=course_id, is_real_data=is_real_data)) > 0


def course_grade_already_exists(course, user, year, semester, is_real_data):
    return len(CourseGrade.objects.filter(course=course, user=user, year=year, semester=semester,
                                          is_real_data=is_real_data)) > 0


def upload_data_to_db(user_name, grades_table, is_real_data=True, update=False):
    """
    uploads the cadet's grades to elements DB, using list of dicts that is given from the
    function pull_student_grades in HujiGradePuller
    :param update: True if want to update exist courses
    :param user_name: fitting hebrew name to talpix
    :param is_real_data: True for inserting real data, false otherwise
    :param grades_table: list of dicts containing the grades and their information of courses
    :return: void
    """
    num_updated = 0
    num_inserted = 0
    for dict in grades_table:
        course_name = dict['course name']
        course_number = dict['course number']
        naz = dict['naz']
        faculty = dict['faculty']
        student_mean = dict['student mean']  # saved for potential use
        year = dict['year']
        moed = dict['moed']
        try:
            not_encrypted_final_grade = float(dict['final grade'])
        except:
            not_encrypted_final_grade = -1
        try:
            not_encrypted_grade_a = float(dict['grade_א'])
        except:
            not_encrypted_grade_a = -1
        final_grade = CourseGrade.encrypt(not_encrypted_final_grade)
        moed_a_grade = CourseGrade.encrypt(not_encrypted_grade_a)
        semester = dict['semester']
        try:
            # check if the course has grade in it
            if not_encrypted_final_grade != -1:
                naz = int(naz[0])
                course_number = int(course_number)

                course = Course(name=course_name, id_number=course_number, credits=naz, field=faculty,
                                is_real_data=is_real_data)
                if not course_already_exists(course_number, is_real_data=is_real_data):
                    course.save()
                else:
                    course = Course.objects.filter(id_number=course_number, is_real_data=is_real_data).first()
                user = User.objects.filter(name=user_name).first()
                if user is None:
                    print(f'user {user_name} not found, can\'t upload {course_name}')
                    continue

                if not course_grade_already_exists(course, user, year, semester, is_real_data):
                    # need to create new course grade
                    course_grade = CourseGrade(course=course, user=user, grade=final_grade, moed=moed, year=year,
                                               semester=semester, moed_a_grade=moed_a_grade, is_real_data=is_real_data)
                    course_grade.save()

                    num_inserted += 1
                else:
                    if not update:
                        print(f'course {course_name} exist for {user_name}, not uploading')
                        continue
                    # the case newer data is given - so need to update
                    exist_course_grade = CourseGrade.objects.filter(course=course, user=user, year=year, semester=semester,
                                                                    is_real_data=is_real_data).first()
                    exist_course_grade.grade = final_grade
                    exist_course_grade.moed = moed
                    exist_course_grade.moed_grade_a = moed_a_grade
                    exist_course_grade.save()
                    num_updated += 1

        finally:
            pass

    print(f'user_name: {user_name}, inserted: {num_inserted}, updated: {num_updated}')
