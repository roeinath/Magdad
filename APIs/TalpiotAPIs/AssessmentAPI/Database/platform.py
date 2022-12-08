from mongoengine import *

from APIs.TalpiotAPIs.AssessmentAPI.Database.api.querycalls.filter import Filter
from APIs.TalpiotAPIs.AssessmentAPI.Database.platform_grade import PlatformGrade


class Platform(Document):
    types = ["פלטפורמה", "הערכה", "תפקיד", "קורס", "סוציומטרי", "התנסות"]
    name = StringField(required=True)
    type = StringField(required=False)
    is_real_data = BooleanField(default=False, required=True)  # boolean if the data is real or not

    meta = {'collection': 'platform'}

    # need to understand all below
    @property
    def platform_grades(self):  # Platforms are uniquely determined by name
        return Filter.matches_query('platform', Filter.is_filter("name",
                                                                 self.name),
                                    Platform).execute(PlatformGrade)

    def get_platform_grades_by_semester(self, semester):
        return [pg for pg in self.platform_grades() if pg.semester == semester]

    def get_talpions_by_semester(self, semester):
        pgs = self.get_platform_grades_by_semester(semester)
        return [pg.talpion for pg in pgs]

    def __str__(self):
        return f"platform: \"{self.name}\""
