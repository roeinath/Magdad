from APIs.TalpiotAPIs.Tasks.task import Task
from APIs.TalpiotAPIs.Tasks.dummy_task import DummyTask
from APIs.TalpiotAPIs.Tasks.task_type import TaskType
from web_features.guardings.guarding_constants import GUARDING_TYPES_IDS


def _calculate_regular_tasks_points(users_by_id):
    """
    Calculated points from regular tasks
    :param users_by_id: a dict of type {user: user_id}
    :return: a dict of type {user: points}
    """
    points_per_task = {task.id: task.points for task in TaskType.objects}
    users_points = {u: 0 for u in users_by_id.values()}
    # group tasks by assigned users and task type, and sum
    pipeline = [
        {
            "$group": {
                "_id": {
                    "users": "$assignment",
                    "type": "$task_type"
                },
                "count": {
                    "$sum": 1
                }
            }
        }
    ]
    aggregated = Task.objects.aggregate(pipeline)
    # doc is dict that has the following shape:
    # {"_id" : {"users": [assigned users], "type": task_type},
    #  "count": the amount of time this object appeared}
    for doc in aggregated:
        if "users" not in doc["_id"]:  # assignment is null
            continue
        for user_id in doc["_id"]["users"]:
            if user_id in users_by_id:  # if user is in mahzor
                user = users_by_id[user_id]
                users_points[user] += points_per_task[doc["_id"]["type"]] * doc["count"]
    return users_points


def _calculate_dummy_task_points(users_by_id):
    """
    Calculated points from dummy tasks
    :param users_by_id: a dict of type {user: user_id}
    :return: a dict of type {user: points}
    """
    users_points = {u: 0 for u in users_by_id.values()}
    # group tasks by assigned users and task type, and sum
    pipeline = [
        {
            "$group": {
                "_id": "$users",
                "total_points": {
                    "$sum": "$points"
                }
            }
        }
    ]
    aggregated = DummyTask.objects.aggregate(pipeline)
    # doc is dict that has the following shape:
    # {"_id" : [users],
    #  "total_points": the number of points to add
    for doc in aggregated:
        for user_id in doc["_id"]:
            if user_id in users_by_id:  # if user is in mahzor
                user = users_by_id[user_id]
                users_points[user] += doc["total_points"]
    return users_points


def calculate_guarding_points(all_users):
    """
    Calculates the guarding points of all users in the all_users list
    :param all_users: a list of users for which to calculate guarding points
    :return: a dict of type {user: points}
    """
    users_by_id = {user.id: user for user in all_users}
    users_points = _calculate_regular_tasks_points(users_by_id)
    users_dummy_points = _calculate_dummy_task_points(users_by_id)

    for user, points in users_dummy_points.items():
        users_points[user] = users_points.get(user, 0) + points

    return users_points
