from datetime import datetime, timedelta

from APIs.TalpiotAPIs.Group.mahzor_group import MahzorGroup
from APIs.TalpiotAPIs.static_fields import get_static_fields


class MahzorsUtilsFields(object):
    def __init__(self) -> None:
        super().__init__()

        ms = get_static_fields().current_mahzors
        self.mahzors = {m: m.mahzor_num for m in ms}

        self.mahzor_year_3 = min(self.mahzors, key=self.mahzors.get)
        self.mahzor_year_1 = max(self.mahzors, key=self.mahzors.get)
        self.mahzor_year_2 = None

        for m in self.mahzors.keys():
            if m != self.mahzor_year_1 and m != self.mahzor_year_3:
                self.mahzor_year_2 = m
                break

        self.mahzors = {m.mahzor_num: m for m in ms}


_utils_fields = MahzorsUtilsFields()


def get_mahzor_year_1():
    return _utils_fields.mahzor_year_1


def get_mahzor_year_2():
    return _utils_fields.mahzor_year_2


def get_mahzor_year_3():
    return _utils_fields.mahzor_year_3


def mahzor_number_to_short_name(mahzor_num):
    if not isinstance(mahzor_num, int):
        mahzor_num = int(mahzor_num)
    return MahzorGroup.objects(mahzor_num=mahzor_num)[0].short_name


def get_mahzor_numbers():
    return [m.mahzor_num for m in _utils_fields.mahzors.values()]


def get_mahzors():
    return _utils_fields.mahzors.values()


def day_of_week_num_to_hebrew_name(day_num):
    hebrew_day_name_dict = {
        0: "יום שני",
        1: "יום שלישי",
        2: "יום רביעי",
        3: "יום חמישי",
        4: "יום שישי",
        5: "יום שבת",
        6: "יום ראשון"
    }
    return hebrew_day_name_dict[day_num]


def get_mahzor_color(mahzor_number):
    last_digit = mahzor_number % 10
    mahzor_colors_dict = {
        0: '#ff8f8f',
        1: '#baf9ff',
        2: '#b8ffb9',
        3: '#fffec2',
        4: '#fec7ff',
        5: '#fffff5',
        6: '#ff8f8f',
        7: '#b8ffb9',
        8: '#ffe2b0',
        9: '#fffec2'
    }
    return mahzor_colors_dict[last_digit]


def translate_day_name(day_name_english):
    hebrew_day_name_dict = {
        "Sunday": "ראשון",
        "Monday": "שני",
        "Tuesday": "שלישי",
        "Wednesday": "רביעי",
        "Thursday": "חמישי",
        "Friday": "שישי",
        "Saturday": "שבת"
    }
    return hebrew_day_name_dict[day_name_english]


def get_hebrew_time(time_):
    day_name = translate_day_name(time_.strftime("%A"))
    return time_.strftime("%d.%m.%y (") + day_name + ") " + time_.strftime("%H:%M")


def get_current_sunday():
    today = datetime.today().date()
    if today.weekday() == 4 or today.weekday() == 5:
        curr_sunday = today + timedelta(days=(6 - today.weekday()) % 7)
    else:
        curr_sunday = today + timedelta(days=-((1 + today.weekday()) % 7))
    return curr_sunday
