# עבודה עם Google Calendar

ניתן לעבוד עם Google Calendar באמצעות ספריית `ExternalAPIs.GoogleCalendar`.

## האובייקט CalendarEvent

אובייקטי CalendarEvent מתארים אירועים ביומן. אובייקט כזה לא מקושר לאירוע ביומן מיצירתו, ושינויים באובייקט לא משפיעים אוטומטית על היומן.

ניתן ליצור אובייקטים כאלו באמצעות הבנאי:
``` python
CalendarEvent(title: str,
              start_time: Union[datetime, date],
              end_time: Union[datetime, date],
              location: str,
              attendees: list=None,
              creator: str=None,
              calendar_event_id: str=None)
```

| משתנה | הסבר |
| ------ | ------ |
| title | שם האירוע שיופיע ככותרת שלו ביומן |
| start_time, end_time | אובייקטי `datetime` או `date` המתארים את זמני תחילת וסיום האירוע. תשתמשו ב`datetime` כאשר האירוע מתחיל בזמן מוגדר, וב`date` כאשר אתם מתארים אירוע שמתרחש **כל היום**. |
| location | מיקום האירוע שיופיע ביומן | 
| attendees | רשימה של אובייקטי `User` של המוזמנים לאירוע ביומן |
| creator | (לא חובה - נוצר אוטומטית) האימייל של יוצר האירוע |
| calendar_event_id | (לא חובה - נוצר אוטומטית) מספר מזהה המתאים את האובייקט לאירוע מסוים שקיים בGoogle Calendar |

ניתן לקבל תיאור של האובייקט כמילון של מחרוזות באמצעות הפונקציה `()get_data_dict`.

## יצירת אירועים ביומן, עדכון ומחיקה

ניתן לבצע פעולות ביומן באמצעות הפונקציות של האובייקט המוחזר ע"י הקריאה `()GoogleCalendar.get_instance`. כדי לקרוא לפונקציה זאת, צריך להשתמש ב`with` בצורה הבאה:
```python
with GoogleCalendar.get_instance() as gc:
    ... usage of gc ...
```

יצירת אירוע נעשית באמצעות הפונקציה הבאה:
``` python
insert_event(calendar_id: str, event: CalendarEvent, send_updates: str = SEND_UPDATES_ALL) -> CalendarEvent
```


| משתנה | הסבר |
| ------ | ------ |
| calendar_id | המזהה של היומן בו רוצים ליצור את האירוע, מהצורה `AAAAAAAAAAAAAAAAAAAAAAAAAA@group.calendar.google.com`. ניתן לגלות את המזהה של יומן מסויים בעמוד ההגדרות של היומן (תחת `מזהה היומן` או `Calendar ID`). |
| event | אובייקט `CalendarEvent` המתאר את האירוע שרוצים ליצור. הפונקציה **משנה את האובייקט** כך שיתאים לאירוע שנוצר (שימו לב! שינויים באובייקט עדיין לא ישנו אוטומטית את האירוע ביומן). בנוסף, הפונקציה מחזירה את האובייקט. |
| send_updates | למי לשלוח עדכונים על יצירת האירוע. האפשרויות:
- `google_calendar.SEND_UPDATES_ALL` יעדכן את כל המוזמנים (זוהי ברירת המחדל)
- `google_calendar.SEND_UPDATES_EXTERNAL_ONLY` שולח הזמנה רק למשתמשים שהמייל שלהם לא של גוגל
- `google_calendar.SEND_UPDATES_NONE` לא ישלח עדכון לאף אח מהמוזמנים | 


לאחר יצירת האירוע ניתן לשנות את אובייקט ה-`CalendarEvent`. כדי לעדכן אירוע ביומן לפי השינויים באובייקט, או כדי למחוק אירוע מהיומן, ניתן להשתמש בפונקציות הבאות:

``` python
update_event(calendar_id: str, event: CalendarEvent, send_updates: str = SEND_UPDATES_ALL) -> CalendarEvent
delete_event(calendar_id: str, event: CalendarEvent, send_updates: str = SEND_UPDATES_ALL) -> bool
```

הפונקציה `update_event` תחזיר את האירוע ששונה בהצלחה או `None` במקרה של כשלון. `delete_event` תחזיר `True` בהצלחה ו-`False` בכשלון.

משמעות הארגומנטים זהה לאלו של `insert_event`.

## קריאת אירועים מיומן

ניתן לקרוא אירועים מיומן מסויים בטווח זמנים רצוי באמצעות הפונקציה הבאה של האובייקט המוחזר מ-`()GoogleCalendar.get_instance`:

``` python
get_events(calendar_id: str, start_time: datetime, end_time: datetime, max_results: int = 2500) -> List[CalendarEvent]:
```

| משתנה | הסבר |
| ------ | ------ |
| calendar_id | המזהה של היומן בו רוצים ליצור את האירוע, מהצורה `AAAAAAAAAAAAAAAAAAAAAAAAAA@group.calendar.google.com`. ניתן לגלות את המזהה של יומן מסויים בעמוד ההגדרות של היומן (תחת `מזהה היומן` או `Calendar ID`). |
| start_time, end_time | אובייקטי `datetime` שתוחמים את החיפוש |
| max_result | המספר המקסימלי של אירועים שרוצים לקבל. | 
