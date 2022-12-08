from __future__ import annotations

from APIs.TalpiotAPIs.CleaningTasks.cleaning_task import CleaningTask
from APIs.TalpiotAPIs.mahzors_utils import *
from web_features.cleaning_duties.logic.generate_cleaning_tasks.week_schedule_creator import *

DAY_TYPE = TaskType.objects(id="6069aeb73a66bc131352dec2")[0]
default_week_schedule = WeekSchedule.get_default_week_schedule()


def create_week_default(sunday: datetime.date, name: str, week_schedule: WeekSchedule = default_week_schedule):
    """
    Creates a week (CleaningWeek) with the deafult Cleanings
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
    year_1 = get_mahzor_year_1().mahzor_num
    year_2 = get_mahzor_year_2().mahzor_num
    year_3 = get_mahzor_year_3().mahzor_num

    week = CleaningWeek(first_date=str(sunday), name=name)
    for i in range(0, 5):
        date = datetime.datetime(sunday.year, sunday.month, sunday.day) + datetime.timedelta(days=i)
        day = CleaningDay(date=date)

        morning_start_time = date + datetime.timedelta(hours=6, minutes=50)
        morning_end_time = date + datetime.timedelta(hours=7, minutes=30)

        evening_start_time = date + datetime.timedelta(hours=18, minutes=0)
        evening_end_time = date + datetime.timedelta(hours=18, minutes=40)

        night_start_time = date + datetime.timedelta(hours=23, minutes=30)
        night_end_time = date + datetime.timedelta(hours=23, minutes=45)

        day.cleaning_duties = []

        if i == 0:  # sunday
            day.cleaning_duties = [
                CleaningTask.new_task(evening_start_time, evening_end_time, 10, required_people=3,  mahzor=year_1),
                CleaningTask.new_task(night_start_time, night_end_time, 10, required_people=1, mahzor=year_1),
                ##########
                CleaningTask.new_task(evening_start_time, evening_end_time, 10, required_people=1, mahzor=year_2),
                CleaningTask.new_task(night_start_time, night_end_time, 10, required_people=1, mahzor=year_2),
                ##########
                CleaningTask.new_task(evening_start_time, evening_end_time, 10, required_people=1, mahzor=year_3),
                CleaningTask.new_task(night_start_time, night_end_time, 10, required_people=1, mahzor=year_3),
            ]
        elif i == 4:  # thursday
            day.cleaning_duties = [
                CleaningTask.new_task(morning_start_time, morning_end_time, 10, required_people=3, mahzor=year_1),
                ##########
                CleaningTask.new_task(morning_start_time, morning_end_time, 10, required_people=1, mahzor=year_2),
                ##########
                CleaningTask.new_task(morning_start_time, morning_end_time, 10, required_people=1, mahzor=year_3),
            ]

        else:  # monday, tuesday, wednesday
            day.cleaning_duties = [
                CleaningTask.new_task(morning_start_time, morning_end_time, 10, required_people=3, mahzor=year_1),
                CleaningTask.new_task(evening_start_time, evening_end_time, 10, required_people=3, mahzor=year_1),
                CleaningTask.new_task(night_start_time, night_end_time, 10, required_people=1, mahzor=year_1),
                ##########
                CleaningTask.new_task(morning_start_time, morning_end_time, 10, required_people=1, mahzor=year_2),
                CleaningTask.new_task(evening_start_time, evening_end_time, 10, required_people=1, mahzor=year_2),
                CleaningTask.new_task(night_start_time, night_end_time, 10, required_people=1, mahzor=year_2),
                ##########
                CleaningTask.new_task(morning_start_time, morning_end_time, 10, required_people=1, mahzor=year_3),
                CleaningTask.new_task(evening_start_time, evening_end_time, 10, required_people=1, mahzor=year_3),
                CleaningTask.new_task(night_start_time, night_end_time, 10, required_people=1, mahzor=year_3),
            ]
        week.days.append(day)

    return week
