from random import shuffle

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.CleaningTasks.cleaning.cleaning_week import CleaningWeek
from APIs.TalpiotAPIs.CleaningTasks.cleaning_task import CleaningTask
from APIs.TalpiotAPIs.CleaningTasks.dummy_cleaning_task import DummyCleaningTask

def get_users_dict_randomized_by_points(users):
    res = get_users_dict_by_points(users)
    print('got_users_dict')
    randomize_same_points(res)
    
    result = []

    for key in sorted(res.keys()):
        result += res[key]

    print(result)
    return result


def get_users_dict_by_points(users):
    res = {}

    users_points = {}
    for task in CleaningTask.objects:
        for u in task.assignment:
            if u not in users_points:
                users_points[u] = 0
            users_points[u] += task.points

    for task in DummyCleaningTask.objects:
        for u in task.users:
            if u not in users_points:
                users_points[u] = 0
            users_points[u] += task.points

    for u in users:
        if u not in users_points:
            users_points[u] = 0
        points = users_points[u]

        if points not in res:
            res[points] = []

        res[points].append(u)

    for key in res.keys():
        print(str(res[key]) + " - " + str(key))

    return res


def randomize_same_points(points_dict):
    for key in points_dict.keys():
        lst = points_dict[key]
        shuffle(lst)
        points_dict[key] = lst


def generate_cleanings(week: CleaningWeek):
    """
    Fills the assignments for the given GuradingWeek,
    according to the mahzor's given in mahzor_selections
    :param week: The week to fill
    :param mahzor_selections:
    :return:
    """
    print('started generating')
    users = {m: get_users_dict_randomized_by_points(User.objects(mahzor=m)) for m in {42, 43, 44} }
    print('pulled data from database')
    for day_number, day in enumerate(week.days):

        for i, task in list(enumerate(day.cleaning_duties)):
            
            mahzor = task.mahzor
            task.assignment = []
            print("Got to assigning: ",task.is_full())
            while not task.is_full():
                usr = users[mahzor].pop(0)
                users[mahzor].append(usr)
                task.assignment.append(usr)
                print("assgined " + usr.name)

            if "__make_calendar_invite" in task:
                task.__make_calendar_invite()
            task.save()

        day.save()

    week.save()

    return True
