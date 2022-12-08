from bot_framework.Activity.FormActivity.Field import TextField
from bot_framework.Activity.FormActivity.form_activity import FormActivity
from bot_features.Shagmach.Classrooms.DBModels.classroom import *

class CreateClassroomForm:
    CLASS_EXISTS = "הכיתה כבר קיימת"
    CLASS_NAME_EMPTY = "חייב לתת לכיתה שם"
    SHORT_CLASS_NAME_EMPTY = "חייב לתת לכיתה שם קצר"

    def __init__(self):
        self.name = TextField(name="שם הכיתה", msg="שם לכיתה בקאלנדר")
        self.short_name = TextField(name="שם קצר לכיתה", msg="שם קצר לכיתה לבוט")

    def validate(self):
        if self.name.value is None:
            raise FormActivity.ValidationException(CreateClassroomForm.CLASS_NAME_EMPTY)
        if self.short_name.value is None:
            raise FormActivity.ValidationException(CreateClassroomForm.SHORT_CLASS_NAME_EMPTY)
        for clas in Classroom.objects:
            if clas.name == self.name.value:
                raise FormActivity.ValidationException(CreateClassroomForm.CLASS_EXISTS)
            if clas.short_name == self.short_name.value:
                raise FormActivity.ValidationException(CreateClassroomForm.CLASS_EXISTS)