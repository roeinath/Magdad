import os.path
from random import shuffle, choice
from scipy.sparse.csgraph import min_weight_full_bipartite_matching
import scipy

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.Tasks.guarding.guarding_week import GuardingWeek
from APIs.TalpiotAPIs.Tasks.task import Task
from APIs.TalpiotAPIs.Tasks.dummy_task import DummyTask
from APIs.TalpiotAPIs.Tasks.task_type import TaskType
from web_features.guardings.guarding_constants import *
from web_features.guardings.logic.calculate_guarding_points import calculate_guarding_points
from collections import Counter
import numpy as np


def can_user_guard(user, task):
    """
    Check if a user can take on the given task (check guarding exemptions)
    :param user: the user
    :param task: the task
    :return: True if the user can guard
    """
    if task.task_type.id == NIGHT_TYPE_ID and user.special_attributes['guarding_exemption'] == GUARDING_EXEMPTION_NIGHT:
        return False

    # if user has no exemption, key 'guarding_exemption' does not exist, so use dict.get to return None
    if user.special_attributes.get('guarding_exemption') == GUARDING_EXEMPTION_TOTAL:
        return False

    return True


def get_guarding_ratios(mahzors_to_choose_from):
    """
    Calculated how many users should guard from each mahzor
    :param mahzors_to_choose_from: the list of mahzors to choose from
    :return: a dict of type {mahzor: the ratio of guards the mahzor should provide}
    """
    guarding_ratio_per_mahzor = {}
    total = 0
    for mahzor in mahzors_to_choose_from:
        l = len(User.objects(mahzor=mahzor))
        guarding_ratio_per_mahzor[mahzor] = l
        total += l
    for key in guarding_ratio_per_mahzor.keys():
        guarding_ratio_per_mahzor[key] = guarding_ratio_per_mahzor[key] / total
    return guarding_ratio_per_mahzor


def _extract_task_groups(week):
    """
    Finds all task_groups in a week
    :param week: the week object
    :return: a list of all task groups in the week
    """
    task_groups = []
    for group in (task.task_group for day in week.days for task in day.guardings):
        if group not in task_groups:
            task_groups.append(group)
    return task_groups


def generate_guardings(week: GuardingWeek, mahzor_selections: dict, do_calendar_invite: bool):
    """
    Fills the assignments for the given GuradingWeek,
    according to the mahzor's given in mahzor_selections
    :param week: The week to fill
    :param mahzor_selections: a dict of type {Task: [mahzors]} where mahzors are the mahzors which can be assigned
    to the task
    :param do_calendar_invite: whether to update Google Calendar invitations
    :return:
    """
    print("starting to generate")

    mahzors_to_choose_from = []
    for selection in mahzor_selections.values():
        for m in selection:
            if m not in mahzors_to_choose_from:
                mahzors_to_choose_from.append(m)

    task_groups = _extract_task_groups(week)

    users_sorted_by_points = {}

    for mahzor in mahzors_to_choose_from:
        users_points = calculate_guarding_points(User.objects(mahzor=mahzor).all())
        users_points_sorted = list(users_points.keys())
        users_points_sorted.sort(key=lambda user: users_points[user])

        users_sorted_by_points[mahzor] = users_points_sorted

    ratios = get_guarding_ratios(mahzors_to_choose_from)
    total_required = len(task_groups)
    assigned_per_mahzor = {m: int(ratios[m] * total_required) for m in mahzors_to_choose_from if m != 0}
    remaining = total_required - sum(assigned_per_mahzor.values())
    for i in range(remaining):
        remaining_percentage_per_mahzor = {m: max(ratio - assigned_per_mahzor[m] / total_required, 0) for m, ratio in
                                           ratios.items()}
        # assign more users, based on fair probabilities
        probabilities = np.array(list(remaining_percentage_per_mahzor.values()), dtype=float)
        print(probabilities)
        probabilities /= probabilities.sum()
        assigned_per_mahzor[np.random.choice(list(remaining_percentage_per_mahzor.keys()),
                                             p=probabilities)] += 1

    if total_required != sum(assigned_per_mahzor.values()):
        return False

    guards = {}
    potential_guards = 0
    guards_list = []
    for m, n_guards in assigned_per_mahzor.items():
        guards[m] = [user for user in users_sorted_by_points[m]
                     if user.special_attributes.get("guarding_exemption") != GUARDING_EXEMPTION_TOTAL]
        potential_guards += len(guards[m])
        guards_list += guards[m]
    shuffle(guards_list)

    # connect all guards to source and all task_groups to sink
    csr_matrix = scipy.sparse.csr_matrix((len(task_groups), potential_guards), dtype=np.int8)

    # generate flow network
    for i, task_group in enumerate(task_groups):
        for j, guard in enumerate(guards_list):
            if all((guard.mahzor in mahzor_selections[subtask] and can_user_guard(guard, subtask) for subtask in
                    task_group)):  # if user can guard all subtasks
                if guard in guards[guard.mahzor][:assigned_per_mahzor[guard.mahzor]]:
                    csr_matrix[i, j] = -2
                else:
                    csr_matrix[i, j] = -1
    # solve
    try:
        i_ind, j_ind = min_weight_full_bipartite_matching(csr_matrix)
    except ValueError:  # cannot possibly be solved
        return False

    for i, j in zip(i_ind, j_ind):
        for task in task_groups[i]:
            task.assignment.append(guards_list[j])

    for day in week.days:
        for task in day.guardings:
            if do_calendar_invite:
                task.update_calendar_invite()
            task.save()
        day.save()
    week.save()

    print("done")

    return True
