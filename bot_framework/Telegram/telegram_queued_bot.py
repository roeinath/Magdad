import traceback
import telegram
from telegram.ext import messagequeue as mq
from bot_framework import crash_logger
from bot_framework.session import Session


class TelegramQueuedBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(TelegramQueuedBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, session: Session, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        try:
            return super(TelegramQueuedBot, self).send_message(*args, **kwargs)
        except:
            report = crash_logger.ErrorReport(session, traceback.format_exc())
            crash_logger.send_report_main_mail(report)
            return None

    @mq.queuedmessage
    def send_photo(self, session: Session, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        try:
            return super(TelegramQueuedBot, self).send_photo(*args, **kwargs)
        except:
            report = crash_logger.ErrorReport(session, traceback.format_exc())
            crash_logger.send_report_main_mail(report)
            return None

    @mq.queuedmessage
    def send_location(self, session: Session, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        try:
            return super(TelegramQueuedBot, self).send_location(*args, **kwargs)
        except:
            report = crash_logger.ErrorReport(session, traceback.format_exc())
            crash_logger.send_report_main_mail(report)
            return None

    @mq.queuedmessage
    def send_contact(self, session: Session, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        try:
            return super(TelegramQueuedBot, self).send_contact(*args, **kwargs)
        except:
            report = crash_logger.ErrorReport(session, traceback.format_exc())
            crash_logger.send_report_main_mail(report)
            return None
