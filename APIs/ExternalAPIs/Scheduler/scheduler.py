import logging
from typing import Callable
# from apscheduler.jobstores.mongodb import MongoDBJobStore
# from apscheduler.schedulers.background import BackgroundScheduler
from APIs.TalpiotSystem import TalpiotSettings




###############################################################################################################

########### THIS DOESNT WORK- APSCHEDULER CAUSE CONFLICTING DEPENDENCIES SO IT WAS REMOVED ####################

###############################################################################################################

class _Scheduler:
    """
    Scheduler object for adding jobs
    """

    def __init__(self):
        """
        Create a scheduler
        """
        # self.scheduler = BackgroundScheduler()
        # self.scheduler.start()
        pass

    def create_job(self, method: Callable, params, year, month, day, hour, minute, day_of_week, start_date, end_date):
        """
        Schedule a job with the given parameters
        """
        # self.scheduler.add_job(method, 'cron', args=params, year=year, month=month, day=day, hour=hour, minute=minute,
        #                       day_of_week=day_of_week,
        #                       start_date=start_date, end_date=end_date)
        pass

    def add_job(self, job):
        """
        Schedule a given ScheduledJob object
        :param job: the job to schedule
        """
        # self.create_job(job.method, job.params, job.year, job.month, job.day, job.hour, job.minute, job.day_of_week,
        #                job.start_date, job.end_date)
        pass


# _scheduler_no_db = _Scheduler()
# logging.getLogger('apscheduler').setLevel(logging.WARNING)


class ScheduledJob:
    """
    Used for creating scheduled "jobs" - methods that will be called at a specific time.
    """

    def __init__(self, method: Callable, params=None, year=None, month=None, day=None,
                 hour=None, minute=None, day_of_week=None, start_date=None, end_date=None):
        """
        Create a new job
        :param method: the method that will be called when the time is right.
        :param params: parameters to call the method with. You can also use lambda.
        :param year: the year the method will be called in. '*' for every year.
        :param month: the month the method will be called in. '*' for every month. Numerical month (4=april and so on).
        :param day: the day of the month the method will be called in. '*' for every day.
        :param hour: the hour the method will be called in. '*' for every hour. 24h clock (15 for 3PM)
        :param minute: the minute the method will be called in. '*' for every minute.
        :param day_of_week: the day of the week the method will be called in.
        :param start_date: a date to start scheduling, this job will not be called before it.
        :param end_date: a date to end scheduling, this job will not be called after it.
        """
        self.method = method
        self.params = params if params else []
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.day_of_week = day_of_week
        self.start_date = start_date
        self.end_date = end_date

    def schedule(self, add_to_db=False):
        """
        Schedule this job to make it start getting called.
        :param add_to_db: True if the job should be added to the db and loaded every bot reset, false otherwise.
        """
        # _scheduler_no_db.add_job(self)
        pass
