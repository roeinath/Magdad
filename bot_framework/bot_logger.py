import inspect
import sys
from inspect import getframeinfo
import os
from enum import Enum
from datetime import datetime


def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def disable():
        BColors.HEADER = ''
        BColors.OKBLUE = ''
        BColors.OKGREEN = ''
        BColors.WARNING = ''
        BColors.FAIL = ''
        BColors.ENDC = ''


class CallerInfo:
    """
    This class is used to give information on the function that called the logger.
    """

    def __init__(self, file: str = None, line: int = None, function: str = None):
        self.file: str = file
        self.line: int = line
        self.function: str = function

    def __str__(self) -> str:
        return f"{self.file}:{self.line} in {self.function}"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def get_caller_info():
        caller_info: CallerInfo = CallerInfo()
        caller_info.file = CallerInfo.get_caller_file()
        caller_info.line = CallerInfo.get_caller_line()
        caller_info.function = CallerInfo.get_caller_function()
        return caller_info

    @staticmethod
    def get_caller_file():
        frames = inspect.stack()
        frame = frames[4]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        return os.path.basename(filename)

    @staticmethod
    def get_caller_line():
        caller = getframeinfo(inspect.stack()[4][0])
        return caller.lineno

    @staticmethod
    def get_caller_function():
        return inspect.stack()[4].function

# if not supports_color():
#     BColors.disable()
#     print(
#         "If you want to see colors in Pycharm, go to Run | Edit Configurations... | Configuration | Emulate terminal in output console")


class LoggingType(Enum):
    INFO = BColors.OKGREEN + "[*] [INFO]" + BColors.ENDC
    WARNING = BColors.WARNING + "[!] [WARNING]" + BColors.ENDC
    SUCCESS = BColors.OKGREEN + "[+] [SUCCESS]" + BColors.ENDC
    FAILURE = BColors.FAIL + "[-] [FAILURE]" + BColors.ENDC
    ERROR = BColors.FAIL + "[!!!] [ERROR]" + BColors.ENDC
    DEBUG = BColors.OKBLUE + "[?] [DEBUG]" + BColors.ENDC


class BotLogger:
    @staticmethod
    def __log(message: str, logging_type: LoggingType = LoggingType.INFO):
        ascii_time = BotLogger.get_time()
        calling_info = CallerInfo.get_caller_info()
        print(f"{logging_type.value} [{ascii_time}] [{calling_info}] [{BColors.OKGREEN}{message}{BColors.ENDC}]")

    @staticmethod
    def get_time():
        now = datetime.now()
        return now.strftime("%H:%M:%S.%f")

    @staticmethod
    def info(message: str):
        BotLogger.__log(message, LoggingType.INFO)

    @staticmethod
    def debug(message: str):
        BotLogger.__log(message, LoggingType.DEBUG)

    @staticmethod
    def warning(message: str):
        BotLogger.__log(message, LoggingType.WARNING)

    @staticmethod
    def error(message: str):
        BotLogger.__log(message, LoggingType.ERROR)

    @staticmethod
    def success(message: str):
        BotLogger.__log(message, LoggingType.SUCCESS)

    @staticmethod
    def failure(message: str):
        BotLogger.__log(message, LoggingType.FAILURE)
