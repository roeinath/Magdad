from abc import ABC
from abc import abstractmethod

from APIs.TalpiotSystem import TBLogger
from bot_framework.CalendarListener.calendar_listener import CalendarListener
from bot_framework.Commands.bot_command_handler import BotCommandHandler
from bot_framework.Scheduling.bot_scheduler import BotScheduler
import os

class BotManager(ABC):

    def __init__(self):
        self.ui = None

    @abstractmethod
    def load_handlers(self):
        pass

    @abstractmethod
    def run(self):
        if 'CONTAINER_NAME' not in os.environ:
            TBLogger.info("Using bot scheduler")
            BotCommandHandler(self.ui)
            BotScheduler.get_scheduler()
            CalendarListener.get_listener()
        else:
            TBLogger.info("Not using bot scheduler")

