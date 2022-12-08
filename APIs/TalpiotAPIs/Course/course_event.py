from __future__ import annotations

from APIs.TalpiotAPIs.Course.course_axis import CourseAxis
from mongoengine import *
from APIs.TalpiotAPIs.Course.course_file import CourseFile


class CourseEvent(Document):

    title = StringField()
    time = DateTimeField()
    axis = ListField(ReferenceField(CourseAxis, reverse_delete_rule=PULL))
    parent = ReferenceField('self', reverse_delete_rule=NULLIFY)
    files = EmbeddedDocumentListField(CourseFile)
