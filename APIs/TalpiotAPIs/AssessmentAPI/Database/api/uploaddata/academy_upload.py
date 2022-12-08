from APIs.TalpiotSystem import TalpiotSettings, TalpiotDatabaseCredentials, Vault
from APIs.TalpiotAPIs.AssessmentAPI.Database.course_grade import CourseGrade
from APIs.TalpiotAPIs.AssessmentAPI.Database.course import Course
from APIs.TalpiotAPIs.User.user import User
import csv

from APIs.init_APIs import main as set_up_DB

"""
    this is file for Academy Grades upload
"""


def save_data_in_mock_db():
    p1 = Course(name="ff", id_number=31231, credits=5, field="kk")
    p2 = CourseGrade(user=get_user_by_name("יואב פלטו"), course=p1, grade=77, semester="A")
    p1.save()
    p2.save()


# TODO finish all uploads in courses

def get_user_by_name(name):
    return User.objects.filter(name=name).first()


def get_course_by_name(name):
    return Course.objects.filter(name=name).first()


if __name__ == "__main__":
    set_up_DB()
    save_data_in_mock_db()
