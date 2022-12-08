from mongoengine import Document, DictField, StringField, DateTimeField, ListField
from typing import Callable
import datetime


# A bot command that should be located in the bot_commands collection
class BotScheduledJob(Document):
    meta = {'collection': 'scheduled_jobs'}

    feature: str = StringField(required=True)
    schedule_time: datetime.datetime = DateTimeField()
    args: list = ListField(required=False)
    kwargs: dict = DictField(required=False)


def remove_by_rule(rule: Callable[[BotScheduledJob], bool]):
    for scheduled_job in BotScheduledJob.objects():
        if rule(scheduled_job):
            print("Scheduled job deleted:\n", scheduled_job.feature, scheduled_job.schedule_time,
                  scheduled_job.args, scheduled_job.kwargs)
            scheduled_job.delete()
