from datetime import datetime, timedelta

from APIs.ExternalAPIs import GoogleDrive, GoogleCalendar, CalendarEvent
from APIs.TalpiotAPIs.LogisticEvents.logistic_event import LogisticEvent
from APIs.TalpiotAPIs.LogisticEvents.logistic_event_status import LogisticEventStatus

DATE_FORMAT = '%d/%m/%Y'
LOGISTIC_EVENTS_DRIVE_ID = "1O6op3fUww1A7S2CkaM0-LKWVfKvytiXU"
LOGISTIC_EVENTS_CALENDAR_ID = "daa69d6874ca3923b72edc981810110cdb6968ebbe1bb7d19a9cfd3e11c163db" \
                              "@group.calendar.google.com"


class LogisticExternalGoogleManager:
    def __init__(self):
        self.google_drive = GoogleDrive.get_instance()
        self.google_calendar = GoogleCalendar.get_instance()

    #########
    # DRIVE #
    #########

    def create_event_folder(self, event: LogisticEvent):
        if event.drive_folder_id:
            return
        folder_name = f"{event.event_name} {event.event_date.strftime(DATE_FORMAT)}"
        folder = self.google_drive.create_folder(folder_name, LOGISTIC_EVENTS_DRIVE_ID)
        return folder['id']

    def add_folder_to_drive(self, logistic_event: LogisticEvent):
        logistic_event.drive_folder_id = self.create_event_folder(logistic_event)
        for status in LogisticEventStatus.objects(event_name=logistic_event.event_name):
            # TODO: move files of status to folder
            pass
        logistic_event.save()

    ############
    # CALENDAR #
    ############

    def insert_event_to_calendar(self, event: LogisticEvent, current_status: LogisticEventStatus):
        start_time = datetime.combine(current_status.deadline, datetime.min.time())

        calendar_event = CalendarEvent(
            title=f"דדליין {current_status.status_name} {event.event_name}",
            start_time=start_time,
            end_time=start_time + timedelta(days=1),
            location='',
            attendees=event.cadets_in_charge + event.sagaz_in_charge + event.sagab_in_charge,
        )
        print(
            f"Inserting event {calendar_event.title} to calendar {LOGISTIC_EVENTS_CALENDAR_ID} at {calendar_event.start_time}"
        )
        calendar_event.save()

        calendar_event = self.google_calendar.insert_event(LOGISTIC_EVENTS_CALENDAR_ID, calendar_event)
        if calendar_event is not None:
            print(f"Event {calendar_event.title} inserted successfully")
            current_status.calendar_event = calendar_event
            calendar_event.save()

    def delete_event_from_calendar(self, event: LogisticEvent):
        for status in LogisticEventStatus.objects(event_name=event.event_name):
            self.delete_status_from_calendar(status)

    def delete_status_from_calendar(self, status: LogisticEventStatus):
        if status.calendar_event:
            print(f"Deleting event {status.calendar_event.title} from calendar")
            self.google_calendar.delete_event(LOGISTIC_EVENTS_CALENDAR_ID, status.calendar_event)
            status.calendar_event = None
            status.save()
