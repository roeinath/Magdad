import math
from datetime import date, datetime, timedelta


def is_exams() -> bool:
    return True


def get_semester_start_date() -> date:
    """
    Returns the date of the starting of the current semester.
    TODO: Make This not a magic number rather take this
          from a dedicated control panel.

    :return: date
    """

    return date(2020, 2, 2)


def get_weekday_sunday_starting(x: date) -> int:
    """
    Returns the weekday of the given date, starting
    at sunday (i.e. Sunday=0, ..., Saturday=6)

    :param x: The date to convert to weekday
    :return: weekday of x date
    """

    return x.isoweekday() % 7


def get_week_start(x: date) -> date:
    """
    Returns the program current week's start date.

    :param x: the date to check the week start for
    :return: date
    """

    return x - timedelta(days=get_weekday_sunday_starting(x))


def get_current_program_week_number() -> int:
    """
    Returns the current week number of the Talpiot
    Program, based on the starting of the semester.

    :return: int the number of the current week
    """

    #  Get current date and semester starting date
    d_week1 = get_semester_start_date()
    d_now = datetime.now().date()

    #  Find the sunday of starting week and sunday of current
    #  week
    sunday_week1 = get_week_start(d_week1)
    sunday_now = get_week_start(d_now)

    #  Calculate numer of weeks by the difference
    return 1 + math.floor((sunday_now - sunday_week1).days / 7)
