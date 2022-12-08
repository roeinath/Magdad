import datetime
import queue
import threading
import time

from APIs.ExternalAPIs import GoogleCalendar, SEND_UPDATES_ALL, SEND_UPDATES_NONE

GUARDING_CALENDAR_ID = 'd9oga6q6ck59ir8i8r4omleqtg@group.calendar.google.com'
GUARDING_CALENDAR_QUEUE = queue.Queue()


def add_invite_to_queue(cl_queue, cl_event, send_updates: str = SEND_UPDATES_NONE, do_update: bool = False):
    cl_queue.put((cl_event, send_updates, do_update))


def delete_invite_from_calendar(calendar_id, cl_event, send_updates: str = SEND_UPDATES_ALL):
    with GoogleCalendar.get_instance() as gc:
        gc.delete_event(calendar_id, cl_event, send_updates)


def get_invites_by_date_span(calendar_id, date_span):
    with GoogleCalendar.get_instance() as gc:
        return gc.get_events(
            calendar_id,
            start_time=datetime.datetime.combine(date_span.start, datetime.datetime.min.time()),
            end_time=datetime.datetime.combine(date_span.end, datetime.datetime.min.time())
        )


def calendar_worker(calendar_queue, calendar_id):
    while True:
        cl_event, send_updates, do_update = calendar_queue.get()
        with GoogleCalendar.get_instance() as gc:
            if do_update:
                event_id = gc.update_event(calendar_id, cl_event, send_updates)
            else:
                event_id = gc.insert_event(calendar_id, cl_event, send_updates).calendar_event_id
            cl_event.calendar_event_id = event_id
            cl_event.save()
        time.sleep(0.08)  # to reach max calendar invites per minute (needs to be >= 0.05)


def init_invitations_worker():
    cl_thread = threading.Thread(target=calendar_worker, args=(GUARDING_CALENDAR_QUEUE, GUARDING_CALENDAR_ID),
                                 daemon=True)
    cl_thread.start()
