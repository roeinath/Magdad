from datetime import datetime
from typing import Optional, List

from APIs.ExternalAPIs.GoogleCalendar.calendar_helper import add_timezone_to_date
from APIs.ExternalAPIs.GoogleCalendar.google_calendar import GoogleCalendar
from APIs.TalpiotAPIs.Classroom.classroom import Classroom
from APIs.TalpiotAPIs.Classroom.classroom_event import ClassroomEvent
from APIs.TalpiotAPIs.User.user import User


def get_google_calendar() -> GoogleCalendar:
    """
    Returns the operating GoogleCalendar connection.

    :return: GoogleCalendar object
    """
    return GoogleCalendar.get_instance()


def get_classroom(name: str) -> Classroom:
    """
    Returns a single classroom from the code given
    a classroom name.

    :param name: Name of classroom in the DB
    :return: Classroom Object
    """

    return Classroom.objects.get(
        name=name
    )


def get_classrooms() -> [Classroom]:
    """
    Returns list of the available Classrooms in the database.

    :return: [Classroom] list
    """
    return Classroom.objects.order_by('name')


def get_classroom_event(event_id: str) -> Optional[ClassroomEvent]:
    """
    Returns the classroom event that fits the given event_id.

    :param event_id: The event id of the database
    :return: Optional[ClassroomEvent]
    """

    result = ClassroomEvent.objects(
        id=event_id
    )

    if len(result) == 0:
        return None

    return result[0]


def insert_classroom_event(classroom: Classroom,
                           start_time: datetime,
                           end_time: datetime,
                           user: User) -> Optional[ClassroomEvent]:
    """
    Inserts the parameters into the db, creates a ClassroomEvent, and in the same time
    updates the event in the calendar.

    :param Classroom classroom: The classroom to insert into
    :param datetime start_time: The starting time of the event
    :param datetime end_time:  The ending time of the event
    :param User user: The user that asked the event
    :return: ClassroomEvent on success, None on failure.
    """

    #  Check if the insert is legal
    if classroom not in get_available_classrooms(start_time, end_time):
        return None

    #  Insert the classroom event
    classroom_event = ClassroomEvent(
        classroom=classroom,
        start_time=start_time,
        end_time=end_time,
        user=user
    )

    classroom_event.save_with_calendar(get_google_calendar())

    return classroom_event


def update_classroom_event(classroom_event: ClassroomEvent) -> Optional[ClassroomEvent]:
    """
    Updates the classroomEvent object in the database and in the same time,
    in the database.

    :param ClassroomEvent classroom_event: The classroomEvent to update
    :return: ClassroomEvent on success, None on failure.
    """

    #  Check if the update is legal
    if classroom_event.classroom not in \
        get_available_classrooms(classroom_event.start_time, classroom_event.end_time, classroom_event):
        return None

    #  Update the event
    classroom_event.save_with_calendar(get_google_calendar())

    return classroom_event


def delete_classroom_event(classroom_event: ClassroomEvent):
    """
    Deletes the classroomEvent from the database and from the GoogleCalendar.

    :param classroom_event: The ClassroomEvent to delete.
    :return: ClassroomEvent
    """
    classroom_event.delete_with_calendar(get_google_calendar())

    return classroom_event


def get_classroom_events_for_classroom(classroom: Classroom,
                                       start_time: datetime=None,
                                       end_time: datetime=None,
                                       ignore_event: ClassroomEvent=None):
    """
    Returns list of all classroom events, for a specific classroom.
    If date is specified, limits events that are in the past.

    :param Classroom classroom: Classroom to find events for
    :param datetime start_time: Search start time
    :param datetime end_time: Search end time
    :param ClassroomEvent ignore_event: An event to ignore (Check the status as if it does not exist)
    This is used for checking the status of the board while editing an ClassroomEvent.
    :return:
    """
    if not isinstance(classroom, Classroom):
        return None

    params = {
        "classroom": classroom,
        "end_time__gt": add_timezone_to_date(datetime.now())
    }

    if ignore_event:
        params["id__ne"] = ignore_event.id

    if start_time is not None and end_time is not None:
        params["start_time__lt"] = end_time
        params["end_time__gt"] = start_time

    events = ClassroomEvent.objects(**params)

    return events


def get_classroom_events_for_user(user: User,
                                  min_time: datetime=add_timezone_to_date(datetime.now())) -> Optional[List[ClassroomEvent]]:
    """
    Returns all classroom events that are in the future
    and are of a specific user.

    :param User user: The User to retrieve from
    :param datetime min_time: The time to start returning from. default is now
    :return: [ClassroomEvent]
    """
    if not isinstance(user, User):
        return None

    return ClassroomEvent.objects(
        user=user,
        end_time__gt=min_time
    ).order_by(
        "+start_time"
    )


def is_classroom_available_at_time(classroom: Classroom,
                                   start_time: datetime,
                                   end_time: datetime,
                                   ignore_event: ClassroomEvent=None) -> Optional[bool]:
    """
    Checks if `classroom` is available (No events at all) between start_time
    and end_time.

    :param classroom: Classroom object to check for
    :param start_time: The starting time (datetime)
    :param end_time: The ending time (datetime)
    :param ClassroomEvent ignore_event: An event to ignore (Check the status as if it does not exist)
    This is used for checking the status of the board while editing an ClassroomEvent.
    :return: True if available, False if not.
    """
    if not isinstance(classroom, Classroom):
        return None

    if not isinstance(start_time, datetime) or not isinstance(end_time, datetime):
        return None

    return len(get_classroom_events_for_classroom(classroom, start_time, end_time, ignore_event)) == 0


def get_available_classrooms(start_time: datetime,
                             end_time: datetime,
                             ignore_event: ClassroomEvent=None) -> [Classroom]:
    """
    Returns a list of available classrooms, that are free
    continually from start_time to end_time.

    :param datetime start_time: Starting time to check (datetime)
    :param datetime end_time: Ending time to check (datetime)
    :param ClassroomEvent ignore_event: An event to ignore (Check the status as if it does not exist)
    This is used for checking the status of the board while editing an ClassroomEvent.
    :return:
    """
    if not isinstance(start_time, datetime) or not isinstance(end_time, datetime):
        return None

    classrooms = get_classrooms()

    return list(filter(
        lambda x: is_classroom_available_at_time(x, start_time, end_time, ignore_event),
        classrooms
    ))

