import time
from datetime import datetime, timedelta, timezone

from dateutil import tz

def add_timezone_to_date(date: datetime) -> datetime:
    """
    Adds the local timezone to a given date.
    :param date: The date to add timezone to
    :return: datetime
    """

    local_timezone = tz.tzlocal()
    return date.replace(tzinfo=local_timezone)


def utc_datetime_to_local_time(date: datetime) -> datetime:
    """
    Converts given datetime in UTC to the local timezone
    :param date: The date to add timezone to
    :return: datetime
    """

    utc_timezone = tz.tzutc()
    local_timezone = tz.tzlocal()
    
    utc = date.replace(tzinfo=utc_timezone)

    return utc.astimezone(local_timezone)


def iso_date_format(date: datetime) -> str:
    """
    Returns the date formatted as ISO format,
    i.e. 2018-10-28T10:50+02:00

    :param datetime date: The date to convert
    :return: str
    """

    return add_timezone_to_date(date).isoformat()
