import datetime

from mongoengine import *

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.Tasks.dummy_task import DummyTask
from APIs.TalpiotAPIs.Tasks.task import Task

s = """ליאור פלג	60
ליאור זומר	60
און מלמד	50
אראל נחום	50
יונתן לוי	50
יונתן גובני	50
יעקב פרטלמן	50
כרמל קרופניק	50
עידו עברי	50
אור סוויסה	40
בר דלאל	40
גיא הראל	40
גילי סטפנסקי	40
גלי מזרחי	40
דולב רונן	40
דור אביסרה	40
דן שמשי	40
דנה פלדמן	40
יהל נקאש	40
יואל זלינגר	40
יובל פרץ	40
יובל פרי	40
מישל זילבר	40
נבו טמיר	40
ניצן ניסן טל	40
נעם דוז'י	40
עדי שפר	40
עומר דור	40
עידו שליט	40
עמית מילוא	40
עמית הראל	40
עמרי רפופורט	40
ענת זמיר	40
פלג כדורי	40
רואי נתנזון	40
רון זכריה	40
רעות-אורה אלבוים	40
שגיא נחושתן	40
שחר דנק	40
שחר יוסף זכריה	40
שלי קגן	40
תומר שראל	40
תומר שטרן	40
תמר וידמן	40
תמר אברהמי	40
אמיר בוחניק	30
אמיר אברמוביץ	30
אמיר דורון גולומב הלמן	30
אמיר עזרא בויאנג'יו	30
אמרי שלום שורץ	30
בן נתן סירוטה	30
דניאל מאיר רפאל הרשקוביץ	30
טל ברוקר	30
טל גורדון	30
יובל פישמן	30
ליבנה בנחמו	30
לשם כהן פלח	30
מתן חדד	30
נדב מורד	30
נוה שרגא שינמן	30
סתיו איל	30
עמית רוט	30
ענבל משעל	30
רום פייביש	30
רועי שרץ	30
רם גולדשטין	30
רפאל קלוטניק	30
שי ריזל	30
שילה דאום	30
תומר ישראלי	30
יוגב מוזס	30
אביב שמש	20
דניאל קלמנסון	20
ליעם עידן לורנץ	10"""

from APIs.TalpiotSystem import Vault
from APIs.settings import load_settings

#  Connect to the relevant DBs
load_settings()
# Vault.get_vault().connect_to_db()


def load_from_backup():
    users = s.split('\n')
    for u in users:
        parts = u.split('\t')
        name = parts[0]
        points = parts[1]

        name = " ".join(name.split())

        task = DummyTask(users=[User.objects(name=name)[0]], points=points, date=datetime.date.today(),
                         description='איחוד שמירות')
        task.save()

        print(name, ": ", points)


def merge_guardings():
    users_points_dict = {}
    for task in Task.objects:
        task: Task = task
        for u in task.assignment:
            if u not in users_points_dict:
                users_points_dict[u] = 0
            users_points_dict[u] += task.task_type.points
    for task in DummyTask.objects:
        task: DummyTask = task
        for u in task.users:
            if u not in users_points_dict:
                users_points_dict[u] = 0
            users_points_dict[u] += task.points

    Task.objects().delete()
    DummyTask.objects().delete()

    for u in users_points_dict.keys():
        task = DummyTask(users=[u], points=users_points_dict[u], date=datetime.date.today(), description='איחוד שמירות')
        task.save()


merge_guardings()
