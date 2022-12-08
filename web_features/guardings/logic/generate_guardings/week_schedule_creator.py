from __future__ import annotations

import datetime
from typing import List, Tuple

from APIs.TalpiotAPIs.Tasks.guarding.guarding_day import GuardingDay
from APIs.TalpiotAPIs.Tasks.task import Task
from APIs.TalpiotAPIs.Tasks.task_type import TaskType


class DaySchedule:
    NIGHT_TYPE = TaskType.objects(id="60735c25b8d8c21a625ef6f2")[0]
    DAY_TYPE = TaskType.objects(id="6069aeb73a66bc131352dec2")[0]
    MENZA_TYPE = TaskType.objects(id="60735c045b21ab8f061de8ef")[0]

    def __init__(self, hours: List[Tuple[str, TaskType]]):
        """
        Creates DaySchedule from list of hours,
        for example:
            [
            "00:00->02:00",
            "17:00->19:20"
            ]
        will create dayschedule with 2 guardings
        :param hours: list of times
        """

        self.hours = list(map(
            DaySchedule.string_into_time_tuple,
            hours
        ))

    @staticmethod
    def string_into_time_tuple(tuple: Tuple[str, TaskType]):
        string, type = tuple

        start_time, end_time = string.split("->")

        start_time = start_time.split(":")
        end_time = end_time.split(":")

        return (
            datetime.time(int(start_time[0]), int(start_time[1])),
            datetime.time(int(end_time[0]), int(end_time[1])),
            type
        )

    @staticmethod
    def get_default_day_schedule() -> DaySchedule:
        return DaySchedule(hours=[
            ("00:00->02:00", DaySchedule.NIGHT_TYPE),
            ("02:00->04:00", DaySchedule.NIGHT_TYPE),
            ("04:00->06:00", DaySchedule.NIGHT_TYPE),
            ("06:00->08:00", DaySchedule.DAY_TYPE),
            ("17:00->19:20", DaySchedule.DAY_TYPE),
            ("18:30->20:30", DaySchedule.MENZA_TYPE),
            ("19:20->21:40", DaySchedule.DAY_TYPE),
            ("21:40->23:59", DaySchedule.DAY_TYPE),
        ])


class WeekSchedule:
    def __init__(self, days: List[DaySchedule]):
        self.days = days

    @staticmethod
    def get_default_week_schedule() -> WeekSchedule:
        return WeekSchedule(days=[
            DaySchedule.get_default_day_schedule(),
            DaySchedule.get_default_day_schedule(),
            DaySchedule.get_default_day_schedule(),
            DaySchedule.get_default_day_schedule(),
            DaySchedule.get_default_day_schedule(),
            DaySchedule.get_default_day_schedule(),
            DaySchedule.get_default_day_schedule(),
        ])


def get_guarding_day(sunday: datetime.date, day: int, day_schedule: DaySchedule):
    """
    Returns GuardingDay from day_schedule
    :param sunday:
    :param day:
    :param day_schedule:
    :return:
    """

    date = sunday + datetime.timedelta(days=day)

    guardings = [
        Task.new_task(datetime.datetime.combine(date, t[0]), datetime.datetime.combine(date, t[1]), t[2]) for t in
        day_schedule.hours
    ]

    return GuardingDay(guardings=guardings, date=date)
