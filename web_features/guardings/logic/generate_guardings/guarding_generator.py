from random import shuffle, choice

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.Tasks.guarding.guarding_week import GuardingWeek
from APIs.TalpiotAPIs.Tasks.task import Task
from APIs.TalpiotAPIs.Tasks.dummy_task import DummyTask
from APIs.TalpiotAPIs.Tasks.task_type import TaskType


def get_all_users_dicts_sorted_by_points(mahzors):
    all_users = []
    for m in mahzors:
        all_users += User.objects(mahzor=m)
    users_points = get_users_points(all_users)
    print("all users points:", users_points)

    res = {}

    for m in mahzors:
        users = User.objects(mahzor=m)
        mahzor_users_by_points = get_users_dict_by_points(users, users_points)

        mahzor_result = []

        for key in sorted(mahzor_users_by_points.keys()):
            mahzor_result += mahzor_users_by_points[key]

        res[m] = mahzor_result
        print(m, ":", mahzor_result)

    return res


def get_users_points(users):
    users_points = {}
    print("getting points from all tasks")
    for task in Task.objects:
        for u in task.assignment:
            if u not in users_points:
                users_points[u] = 0
            users_points[u] += task.task_type.points
    print("done getting tasks, moving to dummy tasks...")
    for task in DummyTask.objects:
        for u in task.users:
            if u not in users_points:
                users_points[u] = 0
            users_points[u] += task.points
    return users_points


def get_users_dict_by_points(users, users_points):
    res = {}
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


def can_user_guard(user, task):
    if task.task_type.id == "60735c25b8d8c21a625ef6f2" and user.special_attributes['guarding_exemption'] == 2:
        return False

    if user.special_attributes['guarding_exemption'] == 1:
        return False

    return True


def get_guarding_ratios(mahzors_to_choose_from, mahzor_selections):
    guarding_ratio_per_mahzor = {}
    total = 0
    for mahzor in mahzors_to_choose_from:
        l = len(User.objects(mahzor=mahzor))
        guarding_ratio_per_mahzor[mahzor] = l
        total += l
    for key in guarding_ratio_per_mahzor.keys():
        guarding_ratio_per_mahzor[key] = guarding_ratio_per_mahzor[key] / total
    return guarding_ratio_per_mahzor


def get_total_guards(week):
    guards = 0
    for day in week.days:
        for task in day.guardings:
            guards += task.task_type.required_people
    return guards


def assign_user(week, user, mahzor_selections):
    if 'guarding_exemption' not in user.special_attributes:
        user.special_attributes['guarding_exemption'] = 0
    if user.special_attributes['guarding_exemption'] == 1:  # a complete exemption means no assignment
        print("user", reversed(str(user)), " has a complete guarding exemption, skipped.")
        return False
    allowed_task_groups = []
    for day in week.days:
        for task in day.guardings:
            if task not in mahzor_selections or mahzor_selections[task] == -1:
                print("task ", task.start_time, "on day", day.date, "removed because no mahzor assigned.")
                day.guardings.remove(task)
                continue
            if len(task.assignment) >= task.task_type.required_people:
                continue
            task_group = task.task_group
            can_guard_all = True
            for subtask in task_group:
                if not (user.mahzor in mahzor_selections[subtask] and can_user_guard(user, subtask)):
                    can_guard_all = False
            if can_guard_all:
                allowed_task_groups.append(task_group)
    if len(allowed_task_groups) == 0:
        print("user", reversed(str(user)), " has no available guardings, skipping.")
        return 0

    chosen_group = choice(allowed_task_groups)
    for task in chosen_group:
        task.assignment.append(user)
    return len(chosen_group)


def generate_guardings(week: GuardingWeek, mahzor_selections: dict, do_calendar_invite: bool):
    """
    Fills the assignments for the given GuradingWeek,
    according to the mahzor's given in mahzor_selections
    :param week: The week to fill
    :param mahzor_selections:
    :param do_calendar_invite:
    :return:
    """
    print("starting to generate")

    mahzors_to_choose_from = []
    for selection in mahzor_selections.values():
        for m in selection:
            if m not in mahzors_to_choose_from:
                mahzors_to_choose_from.append(m)

    print("generate for mahzors: ", mahzors_to_choose_from)

    users = get_all_users_dicts_sorted_by_points(mahzors_to_choose_from)
    assigned_per_mahzor = {m: 0 for m in mahzors_to_choose_from if m != 0}
    ratios = get_guarding_ratios(mahzors_to_choose_from, mahzor_selections)
    total_assigned = 0
    total_required = get_total_guards(week)

    while total_assigned < total_required:

        if len(mahzors_to_choose_from) == 0:
            return False

        print("ratios", ratios)
        selected_mahzor = None
        for m in mahzors_to_choose_from:
            if total_assigned == 0 or assigned_per_mahzor[m] / total_assigned <= ratios[m]:
                selected_mahzor = m
                break

        if selected_mahzor is None:
            return mahzors_to_choose_from[0]

        while True:
            if len(users[m]) == 0:  # no user can be assigned anymore from this mahzor
                print("removing", selected_mahzor, "from available at", total_assigned, "/", total_required,
                      "assignees")
                mahzors_to_choose_from.remove(selected_mahzor)
                break
            u = users[m].pop(0)
            tasks_assigned_to_user = assign_user(week, u, mahzor_selections)
            if tasks_assigned_to_user > 0:  # if assignment is successful
                users[m].append(u)
                assigned_per_mahzor[m] += tasks_assigned_to_user
                total_assigned += tasks_assigned_to_user
                print("Assigned ", reversed(u.name), total_assigned, "/", total_required, "assignees")
                break
            else:
                print("User", reversed(u.name), "cannot guard at", total_assigned, "/", total_required, "assignees")

    for day in week.days:
        for task in day.guardings:
            if do_calendar_invite:
                task.update_calendar_invite()
            task.save()
        day.save()
    week.save()

    print("done")

    return True
