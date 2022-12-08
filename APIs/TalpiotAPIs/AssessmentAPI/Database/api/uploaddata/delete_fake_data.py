from APIs.TalpiotAPIs.AssessmentAPI.Database.course import Course
from APIs.TalpiotAPIs.AssessmentAPI.Database.course_grade import CourseGrade
from APIs.TalpiotAPIs.AssessmentAPI.Database.platform import Platform
from APIs.TalpiotAPIs.AssessmentAPI.Database.platform_grade import PlatformGrade

from APIs.init_APIs import main as set_up_DB


def delete_fake_data(academy=False, platforms=False):
    """
    function for deleting fake data
    :param academy: True iff want to delete academy
    :param platforms: True iff want to delete platforms
    :return:
    """
    set_up_DB()

    if academy:
        for course in Course.objects.filter(is_real_data=False):
            course.delete()

        for course_grade in CourseGrade.objects.filter(is_real_data=False):
            course_grade.delete()

    if platforms:
        for platform in Platform.objects.filter(is_real_data=False):
            platform.delete()

        for platform_grade in PlatformGrade.objects.filter(is_real_data=False):
            platform_grade.delete()

