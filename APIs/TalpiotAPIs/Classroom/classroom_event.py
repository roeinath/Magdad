import datetime
from mongoengine import *

from APIs.ExternalAPIs.GoogleCalendar.calendar_event import CalendarEvent
from APIs.TalpiotAPIs.Classroom.classroom import Classroom
from APIs.TalpiotAPIs.User.user import User

HEBREW_DATE = "תאריך"
HEBREW_START_HOUR = "שעת התחלה"
HEBREW_DURATION = "משך הפגישה (בשעות)"
HEBREW_CLASSROOM = "כיתה"

# -- REAL CALENDAR ID:
CLASSROOM_CALENDER_ID = "eeqbp1vhv9d4t7gc0liu4fktq8@group.calendar.google.com"
# -- TEST CALENDAR ID:
# -- CLASSROOM_CALENDER_ID = "ao9nt3fk1r2ot3p6pae2pjmv98@group.calendar.google.com"


class ClassroomEvent(Document):
    meta = {'collection': 'classroom_event'}

    classroom: Classroom = ReferenceField(Classroom, required=True)
    user: User = ReferenceField(User, required=True)
    start_time: datetime.datetime = DateTimeField(required=True)
    end_time: datetime.datetime = DateTimeField(required=True)

    def get_title(self) -> str:
        """
        Returns the title of the classroom event, that
        will appear in the calendar.

        :return: String with the format "<CLASSROOM> - <USER_NAME>"
        """
        return str(self.classroom.name) \
            + " - " \
            + str(self.user.name)

    def get_full_details(self) -> str:
        """
        Returns full details about the ClassroomEvent, in hebrew.

        :return: String with the format
        """

        return ("{he_date}: {date}\n"
                + "{he_start_hour}: {start_hour}\n"
                + "{he_duration}: {duration}\n"
                + "{he_classroom}: {classroom}\n").format(
            he_date=HEBREW_DATE,
            he_start_hour=HEBREW_START_HOUR,
            he_duration=HEBREW_DURATION,
            he_classroom=HEBREW_CLASSROOM,
            date=self.start_time.strftime("%d/%m/%Y"),
            start_hour=self.start_time.strftime("%H:%M"),
            duration=str(self.end_time - self.start_time),
            classroom=str(self.classroom.name)
        )

    def delete_self(self):
        self.delete()
