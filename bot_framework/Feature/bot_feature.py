from abc import ABC, abstractmethod
from datetime import datetime
from typing import Type, Union

from APIs.TalpiotSystem.bot_scheduled_job import BotScheduledJob
from bot_framework.CalendarListener.calendar_listener import CalendarListener
from bot_framework.Scheduling.bot_scheduler import BotScheduler
from bot_framework.View.view import View
from bot_framework.bot_user import BotUser
from bot_framework.session import Session
from bot_framework.ui.ui import UI


class BotFeature(ABC):

    @abstractmethod
    def __init__(self, ui: UI):
        self.ui = ui
        feature_name = self.get_feature_name()
        bot_scheduler = BotScheduler.get_scheduler()
        bot_scheduler.add_feature_handler(feature_name, self.scheduled_jobs_parser)
        if self.calendar_id:
            calendar_listener: CalendarListener = CalendarListener.get_listener()
            calendar_listener.add_calendar_feature_handler(self.calendar_id, self.calendar_event_parser)

    def schedule_job(self, schedule_time: datetime, *args, **kwargs):
        BotScheduledJob(schedule_time=schedule_time, args=args, kwargs=kwargs, feature=self.get_feature_name()).save()
        print("Scheduled a job")

    def scheduled_jobs_parser(self, *args, **kwargs):
        pass

    def calendar_event_parser(self, calendar_event_id, changed_attributes: dict = None, is_deleted: bool = False):
        pass

    @property
    def calendar_id(self) -> Union[str, None]:
        return None

    def get_feature_name(self) -> str:
        return type(self).__name__

    @abstractmethod
    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """
        pass

    def get_summarize_views(self, session: Session) -> [View]:
        """
        Called externally when the BotManager wants to close this feature.
        This function returns an array of views that summarize the current
        status of the session. The array can be empty.
        :param session: Session object
        :return: Array of views summarizing the current feature Status.
        """
        return []

    @abstractmethod
    def is_authorized(self, user: Type[BotUser]) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        pass
