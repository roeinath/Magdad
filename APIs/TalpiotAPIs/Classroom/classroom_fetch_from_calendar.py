import re
from datetime import datetime
from datetime import timedelta

from APIs.ExternalAPIs.GoogleCalendar.google_calendar import GoogleCalendar
from APIs.TalpiotAPIs.Classroom.classroom import Classroom
from APIs.TalpiotAPIs.Classroom.classroom_event import ClassroomEvent
from APIs.TalpiotAPIs.User.user import User

OLD_CLASSROOM_CALENDAR = "eeqbp1vhv9d4t7gc0liu4fktq8@group.calendar.google.com"
# -- TEST_CLASSROOM_CALENDAR = "ao9nt3fk1r2ot3p6pae2pjmv98@group.calendar.google.com"

# connect_db_readonly_access()

# -- Creates
start_time = datetime.now()
gc = GoogleCalendar()
events = gc.get_events(OLD_CLASSROOM_CALENDAR, start_time, start_time + timedelta(days=3000))

for event in events:
    #  Ignore default reccuring event
    if event.title == """כדי לשריין לכאן כיתות דברו עם השגמ"ח כיתות (:""":
        # print("Skipped default msg")
        continue

    if "סדרת מיון" in event.title:
        print("Skipped sidrat miun")
        continue

    LIBRARY = "(ספרי[י]?[הת])"
    DIUNIM = """(חד[' "]?ן)|(דיונים)"""
    CLASSROOM = """([בג])[׳' "]*?(\d)"""
    GIMELIM_COMPUTERS = """(כיתת מחשבים (קטנה )?ליד תמ[" ]*[מם])|(חדר קטן ליד תממ)"""
    ODITORIOM = "אודיטוריום"
    MOADON = "מועדון"

    # -- Detect the user that ordered this class --
    email = event.creator["email"]

    if email == "yoav.tamir00@gmail.com":
        email = "yoav.tamir.40@gmail.com"

    if email == "talpibotsystem@gmail.com":
        # print("Skipped bot event")
        continue

    user = list(User.objects(
        email=email
    ))

    if len(user) == 0:
        print("User not found for:", email)
        continue

    user = user[0]

    #  -- Detect the classroom ordered ---
    library_matches = re.findall(LIBRARY, event.title)
    diunim_matches = re.findall(DIUNIM, event.title)
    classroom_matches = re.findall(CLASSROOM, event.title)
    gimelim_comp_matches = re.findall(GIMELIM_COMPUTERS, event.title)
    oditoriom_matches = re.findall(ODITORIOM, event.title)
    moadon_matches = re.findall(MOADON, event.title)

    sum = len(library_matches) + len(diunim_matches) +\
          len(classroom_matches) + len(gimelim_comp_matches) +\
          len(oditoriom_matches) + len(moadon_matches)

    if sum == 0:
        print("Not detected for:", event.title)
        continue

    classroom: Classroom = None

    if len(library_matches) > 0:
        #  Is the library
        classroom = Classroom.objects.get(
            name='גימלים - ספריית ביה"ס -- לדבר עם זאב'
        )

    if len(diunim_matches) > 0:
        #  Is the HADAN
        classroom = Classroom.objects.get(
            name="בתים - חדר דיונים"
        )

    if len(classroom_matches) > 0:
        match = classroom_matches[0]

        name = match[0] + match[1]

        try:
            classroom = Classroom.objects.get(
                name=name
            )
        except Exception:
            print("Exception at name", name, event.title, event.start_time)
            continue

    if len(gimelim_comp_matches) > 0:
        classroom = Classroom.objects.get(
            name="גימלים - כיתת מחשבים קטנה"
        )

    if len(oditoriom_matches) > 0:
        classroom = Classroom.objects.get(
            name="כללי - אודיטוריום"
        )

    if len(moadon_matches) > 0:
        classroom = Classroom.objects.get(
            name="כללי - מועדון"
        )

    #  -- Generate classroom event

    #  First try to recieve event with same name
    new_event: ClassroomEvent = None
    try:
        new_event = ClassroomEvent.objects.get(
            calendar_event_id=event.calendar_event_id
        )
        # print("[EXISTS] Detected", classroom.name, ",", user.name, ",", event.title)
        continue
    except:
        new_event = ClassroomEvent()
        print("   [NEW] Detected", classroom.name, ",", user.name, ",", event.title)

    new_event.calendar_event_id = event.calendar_event_id
    new_event.classroom = classroom
    new_event.user = user
    new_event.start_time = event.start_time
    new_event.end_time = event.end_time

    new_event.save()

    # new_event.save_with_calendar(gc, SEND_UPDATES_NONE)


