from bot_framework.Activity.FormActivity.Field import DateField, TimeField
from bot_framework.Activity.FormActivity.form_activity import FormActivity


class OrderClassroomForm:
    BAD_DATE = "בדוק את תקינות התאריך"
    BAD_START_TIME = "בדוק את תקינות שעת התחלה"
    BAD_END_TIME = "בדוק את תקינות שעת סיום"

    def __init__(self):
        self.date = DateField(name="תאריך הזמנה", msg="בחר תאריך להזמנת הכיתה")
        self.start_time = TimeField(name="שעת התחלה", msg="בחר שעת התחלה")
        self.end_time = TimeField(name="שעת סיום", msg="בחר שעת סיום")

    def validate(self):
        if self.date.value is None:
            raise FormActivity.ValidationException(OrderClassroomForm.BAD_DATE)

        if self.start_time.value is None:
            raise FormActivity.ValidationException(OrderClassroomForm.BAD_START_TIME)

        if self.end_time.value is None:
            raise FormActivity.ValidationException(OrderClassroomForm.BAD_END_TIME)
