from mongoengine.fields import IntField
from APIs.ExternalAPIs.GoogleCalendar.calendar_event import CalendarEvent
from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField
import datetime
from APIs.TalpiotAPIs.Tasks.task_type import TaskType
from APIs.TalpiotAPIs.Group.group import Group
from typing import List
from APIs.TalpiotAPIs.User.user import User
from APIs.ExternalAPIs import GoogleCalendar

from APIs.ExternalAPIs.GoogleCalendar.calendar_invite_creator import add_invite_to_queue, GUARDING_CALENDAR_ID, \
    GUARDING_CALENDAR_QUEUE


class CleaningTask(Document):

    start_time: datetime.datetime = DateTimeField()
    end_time: datetime.datetime = DateTimeField()
    points: int = IntField()
    allowed_group: Group = ReferenceField(Group)
    assignment: List[User] = ListField(ReferenceField(User))
    cl_event: CalendarEvent = ReferenceField(CalendarEvent)
    required_people: int = IntField()
    mahzor: int = IntField()

    def is_full(self):
        return self.required_people <= len(self.assignment)

    @staticmethod
    def new_task(start_time: datetime.datetime, end_time: datetime.datetime, points: int, required_people: int = 4, mahzor: int = 0):
        return CleaningTask(start_time=start_time, end_time=end_time, points=points, required_people=required_people, mahzor=mahzor)

    def __make_calendar_invite(self):
        try:
            self.cl_event = CalendarEvent(title="תורנות",
                                          start_time=self.start_time,
                                          end_time=self.end_time,
                                          attendees=self.assignment)
            self.cl_event.save()
        except:
            print("Error making calendar event cleaning_task.py -> make_calendar_invite")
        self.save()

    def update_calendar_invite(self):
        try:
            if self.cl_event and self.cl_event.calendar_event_id:
                with GoogleCalendar.get_instance() as gc:
                    try:
                        gc.delete_event_from_id(GUARDING_CALENDAR_ID, self.cl_event.calendar_event_id)
                    except:
                        self.cl_event.calendar_event_id = None
        except Exception as e:
            # traceback.print_exc()
            print("Error deleting calendar event (cleaning_task.py -> update_calendar_invite)")
        self.__make_calendar_invite()
        add_invite_to_queue(GUARDING_CALENDAR_QUEUE, self.cl_event)


def create_task(start_time, end_time, task_type, allowed_group, assignment):
    t = CleaningTask()
    t.start_time = start_time
    t.end_time = end_time
    t.task_type = task_type
    t.allowed_group = allowed_group
    t.assignment = assignment
    return t