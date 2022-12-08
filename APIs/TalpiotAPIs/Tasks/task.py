from APIs.ExternalAPIs.GoogleCalendar.calendar_event import CalendarEvent
from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField, DoesNotExist
import datetime

from APIs.ExternalAPIs.GoogleCalendar.calendar_invite_creator import add_invite_to_queue, GUARDING_CALENDAR_ID, \
    GUARDING_CALENDAR_QUEUE
from APIs.TalpiotAPIs.Tasks.task_type import TaskType
from APIs.TalpiotAPIs.Group.group import Group
from typing import List
from APIs.TalpiotAPIs.User.user import User
from APIs.ExternalAPIs import GoogleCalendar, SEND_UPDATES_ALL

import traceback


class Task(Document):
    pass


class Task(Document):

    start_time: datetime.datetime = DateTimeField()
    end_time: datetime.datetime = DateTimeField()
    task_type: TaskType = ReferenceField(TaskType)
    allowed_group: Group = ReferenceField(Group)
    assignment: List[User] = ListField(ReferenceField(User))
    cl_event: CalendarEvent = ReferenceField(CalendarEvent)
    cl_event_almash: CalendarEvent = ReferenceField(CalendarEvent)
    task_group: List[Task] = ListField(ReferenceField('self'))

    def is_full(self):
        return self.task_type.required_people <= len(self.assignment)

    @staticmethod
    def new_task(start_time: datetime.datetime, end_time: datetime.datetime, type: TaskType):
        return Task(start_time=start_time, end_time=end_time, task_type=type)

    def __update_cl_event(self):
        try:
            if not self.cl_event or not self.cl_event.calendar_event_id:
                raise DoesNotExist
        except DoesNotExist:
            self.cl_event = CalendarEvent(title="שמירה", start_time=self.start_time, end_time=self.end_time)

        self.cl_event.start_time = self.start_time
        self.cl_event.end_time = self.end_time
        self.cl_event.location = self.task_type.description
        self.cl_event.attendees = self.assignment

        self.cl_event.save()
        add_invite_to_queue(GUARDING_CALENDAR_QUEUE, self.cl_event,
                            do_update=self.cl_event.calendar_event_id is not None)

    def __update_cl_event_almash(self):
        almash_time = self.start_time.replace(hour=16, minute=30)
        # set as the day before
        if self.start_time.time() < datetime.time(hour=16, minute=30):
            almash_time -= datetime.timedelta(days=1)

        try:
            if not self.cl_event_almash or not self.cl_event_almash.calendar_event_id:
                raise DoesNotExist
        except DoesNotExist:
            self.cl_event_almash = CalendarEvent.objects(title="עלמש", start_time=almash_time).first()
            if not self.cl_event_almash:
                self.cl_event_almash = CalendarEvent(title="עלמש", start_time=almash_time,
                                                     end_time=almash_time + datetime.timedelta(minutes=30),
                                                     attendees=[])

        self.cl_event_almash.start_time = almash_time
        self.cl_event_almash.end_time = almash_time + datetime.timedelta(minutes=30)
        self.cl_event_almash.location = "לובי"
        self.cl_event_almash.attendees += self.assignment

        self.cl_event_almash.save()
        add_invite_to_queue(GUARDING_CALENDAR_QUEUE, self.cl_event_almash,
                            do_update=self.cl_event_almash.calendar_event_id is not None)

    def update_calendar_invite(self, send_updates: str = SEND_UPDATES_ALL):
        try:
            self.__update_cl_event()
            self.__update_cl_event_almash()
            self.save()
            return
        except Exception as e:
            traceback.print_exc()
            print("Error updating calendar event (task.py -> update_calendar_invite)")


def create_task(start_time, end_time, task_type, allowed_group, assignment):
    t = Task()
    t.start_time = start_time
    t.end_time = end_time
    t.task_type = task_type
    t.allowed_group = allowed_group
    t.assignment = assignment
    return t
