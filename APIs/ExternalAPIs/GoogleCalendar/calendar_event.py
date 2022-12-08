from typing import Union
from datetime import datetime, date

from APIs.ExternalAPIs.GoogleCalendar.calendar_helper import iso_date_format
from mongoengine import Document, ReferenceField, ListField, StringField, DateField, DateTimeField, DictField
from APIs.TalpiotAPIs.User.user import User

DECLINED = 'declined'
RESPONSE_STATUS = "responseStatus"
CHANGE_ATTRIBUTES = ["title", "start_time", "end_time", "location", "attendees", "non_users_attendees",
                     "creator", "description"]


class CalendarEvent(Document):
    title: str = StringField()
    start_time: datetime = DateTimeField()
    end_time: datetime = DateTimeField()
    location: str = StringField(required=False)
    attendees: list = ListField(ReferenceField(User), default=[])
    non_users_attendees: list = ListField(StringField(), default=[])
    creator: User = ReferenceField(User, required=False)
    description: str = StringField(required=False)

    calendar_event_id: str = StringField()
    calendar_id: str = StringField(required=False)

    @staticmethod
    def new_event(title: str, start_time: datetime, end_time: datetime, location: str, description: str = None,
                  attendees: list = None, creator: dict = None, calendar_event_id: str = None, calendar_id: str = None):
        processed_attendees = []
        non_users_attendees = []
        attendees = attendees or []
        for attendee in attendees:
            response_status = attendee.get(RESPONSE_STATUS, DECLINED)
            if attendee.get("self", False) or response_status == DECLINED:
                continue
            attendee_mail = attendee.get("email", '')
            user_attendee = User.objects(email__iexact=attendee_mail).first()
            if user_attendee:
                processed_attendees.append(user_attendee)
            else:
                non_users_attendees.append(attendee_mail)

        creator = User.objects(email__iexact=creator.get("email", '')).first() or None
        return CalendarEvent(
                title=title,
                start_time=start_time.replace(tzinfo=None),
                end_time=end_time.replace(tzinfo=None),
                location=location,
                description=description,
                attendees=processed_attendees,
                non_users_attendees=non_users_attendees,
                creator=creator,
                calendar_event_id=calendar_event_id,
                calendar_id=calendar_id
            )

    def get_data_dict(self) -> dict:
        """
        Returns dictionary representation of the object, fits to
        send to the Google Calendar API
        :return:
        """
        return {
            'summary': self.title,
            'start': CalendarEvent._get_date_dict(self.start_time),
            'end': CalendarEvent._get_date_dict(self.end_time),
            'attendees': list(map(lambda x: {"email": x.email}, self.attendees)),
            'location': self.location
        }

    def is_all_day(self) -> bool:
        """
        Checks if the event is all-day or not.
        :return: bool
        """

        return type(self.start_time) is date or type(self.end_time) is date

    @staticmethod
    def _get_date_dict(obj: Union[datetime, date]) -> dict:
        if type(obj) is datetime:
            return {'dateTime': iso_date_format(obj)}

        if type(obj) is date:
            return {'date': obj.isoformat()}

        return {}

    def differences(self, other: "CalendarEvent"):
        differences_dict = {}
        for attribute in CHANGE_ATTRIBUTES:
            this_value = getattr(self, attribute, None)
            other_value = getattr(other, attribute, None)
            if this_value != other_value:
                differences_dict[attribute] = {'old': this_value, 'new': other_value}
        return differences_dict

    def __ne__(self, other: "CalendarEvent"):
        return bool(self.differences(other))

    def update(self, other: "CalendarEvent"):
        for attribute in CHANGE_ATTRIBUTES:
            setattr(self, attribute, getattr(other, attribute, None))
        self.save()
