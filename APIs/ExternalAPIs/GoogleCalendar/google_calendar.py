from __future__ import annotations

import json
from typing import Union
import os
import dateutil.parser
from datetime import datetime, date

from APIs.ExternalAPIs.GoogleCalendar.calendar_event import CalendarEvent
from APIs.ExternalAPIs.GoogleCalendar.calendar_helper import iso_date_format
from APIs.ExternalAPIs.WorkerPool.pool import Pool
from APIs.ExternalAPIs.WorkerPool.pooled_worker import PooledWorker

#  If modifying this scopes, delete token.json
from APIs.TalpiotSystem import TalpiotSettings

SCOPES_CALENDAR = ['https://www.googleapis.com/auth/calendar']

SEND_UPDATES_ALL = "all"
SEND_UPDATES_EXTERNAL_ONLY = "externalOnly"
SEND_UPDATES_NONE = "none"

MAX_WORKERS = 5



class GoogleCalendar(PooledWorker):
    """
    A class that allows accessing GoogleCalendar with
    the bot google account.
    """

    _pool = Pool(lambda: GoogleCalendar(), MAX_WORKERS)

    @staticmethod
    def get_instance() -> GoogleCalendar:
        return GoogleCalendar._pool.get_free_worker()

    def __init__(self):
        super().__init__()
        self.creds_diary = None
        self.service = None

        self.connect_to_calendar()

    def connect_to_calendar(self):
        token_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "token.pickle"
        )

        google_settings = TalpiotSettings.get().google_connection_settings
        self.service = google_settings.get_service('calendar', 'v3', scopes=SCOPES_CALENDAR, token_file_path=token_path)

    def get_events(self, calendar_id: str, start_time: datetime, end_time: datetime, max_results: int = 2500):
        """
        Returns all of the events from a calendar with the calendarId
        calendar_id, from start_time to end_time.

        :param calendar_id: The calendar id to retrieve from
        :param start_time: The search start time
        :param end_time: The search end time
        :param max_results: Maximum results to show. Default is 100
        :return: List of CalendarEvent
        """
        result = list()

        # get the data from the diary
        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=iso_date_format(start_time),
            timeMax=iso_date_format(end_time),
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', None)

        for event in events:
            # get the start and the end time of the event
            start_time = GoogleCalendar._parse_google_calendar_date(event['start'])
            end_time = GoogleCalendar._parse_google_calendar_date(event['end'])

            if "summary" not in event:
                event["summary"] = "Busy"

            result.append(CalendarEvent.new_event(
                title=event["summary"],
                start_time=start_time,
                end_time=end_time,
                location=event.get("location", None),
                attendees=event.get("attendees", []),
                creator=event.get("creator", None),
                description=event.get("description", None),
                calendar_event_id=event.get("id", None),
                calendar_id=calendar_id
            ))

        return result

    def insert_event(self, calendar_id: str, event: CalendarEvent, send_updates: str = SEND_UPDATES_ALL):
        """
        Inserts a CalendarEvent into the given calendar
        using self.calendarId.

        :param calendar_id: The calendarId to change
        :param event: The CalendarEvent to update
        :param send_updates: Whether to send updates on the change
        :return: None on failure, CalendarEvent on success.
        """

        try:
            result = self.service.events().insert(
                calendarId=calendar_id,
                body=event.get_data_dict(),
                sendUpdates=send_updates
            ).execute()
        except Exception as e:
            print(f"ERROR: {e}")
            return None

        if "id" not in result:
            print(f"ERROR: {result}")
            return None

        event.calendar_event_id = result["id"]

        return event

    def update_event(self, calendar_id: str, event: CalendarEvent, send_updates: str = SEND_UPDATES_ALL):
        """
        Updates a given CalendarEvent in the calendar,
        referenced to a google calendar event using
        `event.calendar_event_id`.

        :param calendar_id: The calendarId to change
        :param event: The CalendarEvent to update
        :param send_updates: Whether to send updates on the change
        :return: None on failure, CalendarEvent on success
        """

        result = self.service.events().update(
            calendarId=calendar_id,
            eventId=event.calendar_event_id,
            body=event.get_data_dict(),
            sendUpdates=send_updates
        ).execute()

        if "id" not in result:
            return None

        event.calendar_event_id = result["id"]

        return event


    def delete_event_from_id(self, calendar_id: str, event_id: str, send_updates: str = SEND_UPDATES_ALL):
        """
        Deletes a given event from the google calendar based on the event id,
        referenced to a google calendar event using
        `event.calendar_event_id`.

        :param calendar_id: The calendarId to change
        :param event: The CalendarEvent to update
        :param send_updates: Whether to send updates on the change
        :return: False on failure, True on success
        """
        result = self.service.events().delete(
            calendarId=calendar_id,
            eventId=event_id,
            sendUpdates=send_updates
        ).execute()

        if len(result) == 0:
            return True

        return False

    def delete_event(self, calendar_id: str, event: CalendarEvent, send_updates: str = SEND_UPDATES_ALL):
        """
        Deletes a given CalendarEvent from the google calendar,
        referenced to a google calendar event using
        `event.calendar_event_id`.

        :param calendar_id: The calendarId to change
        :param event: The CalendarEvent to update
        :param send_updates: Whether to send updates on the change
        :return: False on failure, True on success
        """
        result = self.service.events().delete(
            calendarId=calendar_id,
            eventId=event.calendar_event_id,
            sendUpdates=send_updates
        ).execute()

        if len(result) == 0:
            return True

        return False

    @staticmethod
    def _parse_google_calendar_date(date_dict: dict) -> Union[datetime, date]:
        if "dateTime" in date_dict:
            return dateutil.parser.parse(date_dict.get("dateTime"))

        if "date" in date_dict:
            return dateutil.parser.parse(date_dict.get("date")).date()


if __name__ == "__main__":
    from datetime import timedelta
    TalpiotSettings()
    with GoogleCalendar.get_instance() as gc:
        print(gc.get_events(
            'talpibotsystem@gmail.com',
            start_time=datetime.now() - timedelta(days=1),
            end_time=datetime.now() + timedelta(days=1),
        ))
