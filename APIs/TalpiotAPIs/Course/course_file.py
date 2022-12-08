from mongoengine import *
from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.Course.course_file_type import CourseFileType


class CourseFile(EmbeddedDocument):

    title = StringField()
    uploader = ReferenceField(User)
    course_file_type = ReferenceField(CourseFileType)
    file = FileField()
    file_name = StringField()
