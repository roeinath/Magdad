from __future__ import annotations

from APIs.TalpiotAPIs.Tasks.guarding.guarding_week import GuardingWeek
from web_features.guardings.logic.generate_guardings.week_schedule_creator import *


def create_week_default(sunday: datetime.date, name: str,
                        week_schedule: WeekSchedule = WeekSchedule.get_default_week_schedule()):
    """
    Creates a week (GuardingWeek) with the deafult guardings
    (Sunday-Thursday:
        0000-0200
        0200-0400
        0400-0600
        0600-0800
        1700-1920
        1920-2140
        2140-0000)

    Starting at the sunday date, and names it with the given name
    :param sunday: Date
    :param name: String
    :param week_schedule: WeekSchedule
    :return:
    """
    NIGHT_TYPE = TaskType.objects(id="60735c25b8d8c21a625ef6f2")[0]
    DAY_TYPE = TaskType.objects(id="6069aeb73a66bc131352dec2")[0]
    DAY_WORK_TYPE = TaskType.objects(id="61c4848b075260f9537105f8")[0]
    MENZA_TYPE = TaskType.objects(id="60735c045b21ab8f061de8ef")[0]
    FRANCE_TYPE = TaskType.objects(id="615c25264691abbcfea9c185")[0]

    week = GuardingWeek(first_date=str(sunday), name=name)
    for i in range(0, 5):
        date = datetime.datetime(sunday.year, sunday.month, sunday.day) + datetime.timedelta(days=i)
        day = GuardingDay(date=date)

        t_17 = Task.new_task(date + datetime.timedelta(days=0, hours=17, minutes=0),
                             date + datetime.timedelta(days=0, hours=19, minutes=20), DAY_TYPE)
        t_17_work = Task.new_task(date + datetime.timedelta(days=0, hours=17, minutes=0),
                                  date + datetime.timedelta(days=0, hours=19, minutes=20), DAY_WORK_TYPE)
        t_19 = Task.new_task(date + datetime.timedelta(days=0, hours=19, minutes=20),
                             date + datetime.timedelta(days=0, hours=21, minutes=40), DAY_TYPE)
        t_19_work = Task.new_task(date + datetime.timedelta(days=0, hours=19, minutes=20),
                                  date + datetime.timedelta(days=0, hours=21, minutes=40), DAY_WORK_TYPE)
        t_menza = Task.new_task(date + datetime.timedelta(days=0, hours=18, minutes=30),
                                date + datetime.timedelta(days=0, hours=20, minutes=30), MENZA_TYPE)
        t_21 = Task.new_task(date + datetime.timedelta(days=0, hours=21, minutes=40),
                             date + datetime.timedelta(days=1, hours=00, minutes=00), DAY_TYPE)
        t_21_work = Task.new_task(date + datetime.timedelta(days=0, hours=21, minutes=40),
                                  date + datetime.timedelta(days=1, hours=00, minutes=00), DAY_WORK_TYPE)
        t_00 = Task.new_task(date + datetime.timedelta(days=1, hours=0, minutes=0),
                             date + datetime.timedelta(days=1, hours=2, minutes=0), NIGHT_TYPE)
        t_02 = Task.new_task(date + datetime.timedelta(days=1, hours=2, minutes=0),
                             date + datetime.timedelta(days=1, hours=4, minutes=0), NIGHT_TYPE)
        t_04 = Task.new_task(date + datetime.timedelta(days=1, hours=4, minutes=0),
                             date + datetime.timedelta(days=1, hours=6, minutes=0), NIGHT_TYPE)
        t_06 = Task.new_task(date + datetime.timedelta(days=1, hours=6, minutes=0),
                             date + datetime.timedelta(days=1, hours=8, minutes=0), DAY_TYPE)
        t_06_work = Task.new_task(date + datetime.timedelta(days=1, hours=6, minutes=0),
                                  date + datetime.timedelta(days=1, hours=8, minutes=0), DAY_WORK_TYPE)
        t_17_france = Task.new_task(date + datetime.timedelta(days=0, hours=16, minutes=50),
                                    date + datetime.timedelta(days=0, hours=19, minutes=20), FRANCE_TYPE)
        t_19_france = Task.new_task(date + datetime.timedelta(days=0, hours=19, minutes=20),
                                    date + datetime.timedelta(days=0, hours=21, minutes=40), FRANCE_TYPE)
        t_21_france = Task.new_task(date + datetime.timedelta(days=0, hours=21, minutes=40),
                                    date + datetime.timedelta(days=1, hours=0, minutes=0), FRANCE_TYPE)
        t_08_france = Task.new_task(date + datetime.timedelta(days=1, hours=8, minutes=0),
                                    date + datetime.timedelta(days=1, hours=10, minutes=15), FRANCE_TYPE)
        t_10_france = Task.new_task(date + datetime.timedelta(days=1, hours=10, minutes=15),
                                    date + datetime.timedelta(days=1, hours=12, minutes=30), FRANCE_TYPE)
        t_12_france = Task.new_task(date + datetime.timedelta(days=1, hours=12, minutes=30),
                                    date + datetime.timedelta(days=1, hours=14, minutes=45), FRANCE_TYPE)
        t_14_france = Task.new_task(date + datetime.timedelta(days=1, hours=14, minutes=45),
                                    date + datetime.timedelta(days=1, hours=16, minutes=40), FRANCE_TYPE)

        guard1_group = [t_17, t_08_france]
        guard2_group = [t_17_work, t_00]
        guard3_group = [t_17_france, t_04]
        guard4_group = [t_menza, t_06_work]
        guard5_group = [t_19, t_21_france]
        guard6_group = [t_06, t_19_work]
        guard7_group = [t_19_france, t_10_france]
        guard8_group = [t_12_france, t_21]
        guard9_group = [t_14_france, t_21_work]
        guard10_group = [t_02]

        groups = [guard1_group, guard2_group, guard3_group, guard4_group, guard5_group, guard6_group, guard7_group,
                  guard8_group, guard9_group, guard10_group]

        day.guardings = [
            t_17,
            t_17_work,
            t_19,
            t_19_work,
            t_menza,
            t_21,
            t_21_work,
            t_00,
            t_02,
            t_04,
            t_06,
            t_06_work,
            t_17_france,
            t_19_france,
            t_21_france,
            t_08_france,
            t_10_france,
            t_12_france,
            t_14_france,
        ]

        for t in day.guardings:
            t.save()

        for g in groups:
            for t in g:
                t.task_group = g

        for t in day.guardings:
            t.save()

        week.days.append(day)

    return week
