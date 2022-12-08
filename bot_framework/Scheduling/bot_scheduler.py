from datetime import datetime
import time
from typing import *
from APIs.TalpiotSystem.bot_scheduled_job import BotScheduledJob
import _thread


# This singleton class is a thread that listens to the botCommand collection and executes the commands it receives
class BotScheduler:
    __instance = None

    def __init__(self):
        if BotScheduler.__instance is not None:
            raise Exception("This class is a singleton!")

        # The function that the handler needs to run for each name of command
        self.feature_names_to_funcs = {}
        self.initialized = False
        _thread.start_new_thread(self.scheduled_jobs_handler, ())

        BotScheduler.__instance = self

    @staticmethod
    def get_scheduler():
        if BotScheduler.__instance is None:
            BotScheduler()
        return BotScheduler.__instance

    # Adds a command to the dict that connects between command names to command functions
    def add_feature_handler(self, feature_name: str, job: Callable):
        if feature_name not in self.feature_names_to_funcs:
            self.feature_names_to_funcs[feature_name] = job
        else:
            print(f"The bot scheduled job feature with the name: '{feature_name}' "
                  f"already exists, try renaming your feature")
            print("This handler was skipped.")
        self.initialized = True

    # Checks for new bot commands in the collection and executes them
    def scheduled_jobs_handler(self):
        SLEEP_TIME = 10
        START_UP_TIME = 30
        time.sleep(START_UP_TIME)
        while True:
            if self.initialized:
                scheduled_jobs = BotScheduledJob.objects()
                for job in scheduled_jobs:
                    if job.schedule_time <= datetime.now():
                        try:
                            self.switch_parser(job)
                        except Exception as err:
                            print(f"Error when executing scheduled job {job}:\n{err}")
                        job.delete()
            time.sleep(SLEEP_TIME)

    # interpret the command and calls it's function
    def switch_parser(self, scheduled_job: BotScheduledJob):
        def on_scheduled_job_not_found(*args, **kwargs):
            print(f"Error: scheduled job {scheduled_job.feature} not found")

        command_function = self.feature_names_to_funcs.get(scheduled_job.feature, on_scheduled_job_not_found)
        command_function(*scheduled_job.args, **scheduled_job.kwargs)
