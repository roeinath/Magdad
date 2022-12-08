import _thread
import time
from datetime import datetime, timedelta
from typing import Callable

from APIs.ExternalAPIs import GoogleCalendar, CalendarEvent
from APIs.TalpiotSystem.calendar_command import CalendarCommand


class CalendarListener:
    __instance = None

    def __init__(self):
        if CalendarListener.__instance is not None:
            raise Exception("This class is a singleton!")

        self.google_calendar = GoogleCalendar.get_instance()
        _thread.start_new_thread(self.calendar_listener, ())

        self.calendar_id_to_funcs = {}
        self.initialized = False

        CalendarListener.__instance = self

    @staticmethod
    def get_listener():
        if CalendarListener.__instance is None:
            CalendarListener()
        return CalendarListener.__instance

    # Adds a command to the dict that connects between command names to command functions
    def add_calendar_feature_handler(self, calendar_id: str, handler: Callable):
        if calendar_id not in self.calendar_id_to_funcs:
            self.calendar_id_to_funcs[calendar_id] = handler
        else:
            print(f"The bot calendar feature with the name: '{calendar_id}' "
                  f"already exists, try renaming your feature")
            print("This handler was skipped.")
        self.initialized = True

    # Checks for new bot commands in the collection and executes them
    def calendar_listener(self):
        SLEEP_TIME = 10
        while True:
            for calendar_id in self.calendar_id_to_funcs:
                events = self.google_calendar.get_events(calendar_id, start_time=datetime.today(),
                                                         end_time=datetime.today() + timedelta(days=6))
                for event in events:
                    command = CalendarCommand.objects(calendar_event_id=event.calendar_event_id).first()
                    saved_event = CalendarEvent.objects(calendar_event_id=event.calendar_event_id).first()

                    differences_dict = saved_event.differences(event) if saved_event else {}

                    if command is None:
                        command = CalendarCommand.new_calendar_command(event)
                    elif len(differences_dict) > 0:
                        saved_event.update(event)
                        command.update(event)
                    else:
                        continue

                    self.calendar_id_to_funcs[calendar_id](command.calendar_event_id,
                                                           changed_attributes=differences_dict,
                                                           is_deleted=False)
                    command.handle()

                calendar_event_id_list = [event.calendar_event_id for event in events]
                deleted_event_list = CalendarEvent.objects(calendar_id=calendar_id,
                                                           calendar_event_id__nin=calendar_event_id_list)
                for deleted_event in deleted_event_list:
                    calendar_event_id = deleted_event.calendar_event_id
                    print(f"deleted event: {deleted_event.title}, {deleted_event.description}")
                    self.calendar_id_to_funcs[calendar_id](calendar_event_id, changed_attributes={},  is_deleted=True)
                    for command in CalendarCommand.objects(calendar_event_id=calendar_event_id):
                        command.delete()
                    deleted_event.delete()

            time.sleep(SLEEP_TIME)

    # # interpret the command and calls it's function
    # def switch_parser(self, scheduled_job: BotScheduledJob):
    #     def on_scheduled_job_not_found(*args, **kwargs):
    #         print(f"Error: scheduled job {scheduled_job.feature} not found")
    #
    #     command_function = self.feature_names_to_funcs.get(scheduled_job.feature, on_scheduled_job_not_found)
    #     command_function(*scheduled_job.args, **scheduled_job.kwargs)
