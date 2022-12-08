from datetime import datetime

from mongoengine import Document, StringField, BooleanField, DateTimeField

from APIs.ExternalAPIs import CalendarEvent


class CalendarCommand(Document):
    calendar_event_id: str = StringField(required=True)
    title: str = StringField(required=False)
    is_handled: bool = BooleanField(required=True, default=False)

    @staticmethod
    def new_calendar_command(calendar_event: CalendarEvent) -> "CalendarCommand":
        calendar_event.save()
        return CalendarCommand(calendar_event_id=calendar_event.calendar_event_id, title=calendar_event.title,
                               is_handled=False).save()

    def update(self, calendar_event: CalendarEvent):
        self.calendar_event_id = calendar_event.calendar_event_id
        self.title = calendar_event.title
        self.save()

    def handle(self):
        self.is_handled = True
        self.save()
