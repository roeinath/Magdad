from mongoengine import *

from APIs.TalpiotAPIs.AssessmentAPI.Database.api.querycalls.filter import Filter
from APIs.TalpiotAPIs.AssessmentAPI.Database.course_grade import CourseGrade


class Course(Document):
    name = StringField()
    id_number = IntField()
    credits = IntField()
    field = StringField()
    is_real_data = BooleanField(default=False, required=True)  # boolean if the data is real or not
    student_mean_per_year = DictField(required=False)

    meta = {"collection": "course"}

    @property
    def course_grades(self):  # Courses are uniquely determined by ID
        return Filter.matches_query('course', Filter.is_filter("id_number",
                                                               self.id_number),
                                    Course).execute(CourseGrade)

    def get_numeral_course_grades(self):
        return [cg.grade for cg in self.course_grades]

    def get_course_grades_by_semester(self, semester):
        return [cg for cg in self.course_grades if cg.semester == semester]

    def __str__(self):
        return f"{self.name}"
