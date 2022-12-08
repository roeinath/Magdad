from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.Group.group import Group

from typing import List


def get_user_groups(user: User) -> List[Group]:
    """
    Get all groups with a certain user in their participants.
    Args:
        user: The user to find its groups.

    Returns: All Groups with the user in their participants.

    """
    groups = []
    for group in Group.objects:
        if user in group.participants:
            groups.append(group)
    return list(groups)


def is_user_in_group_name(user: User, group_name):
    groups_found = Group.objects(name=group_name)
    if len(groups_found) == 0:
        print("Tried to find group name ", group_name, " that doesn't exist")
        return False
    return user in Group.objects(name=group_name)[0]


def is_user_in_group(user: User, group: Group):
    return user in group


def is_user_in_group_type(user: User, group_type):
    for group in group_type.objects:
        if user in group.participants:
            return True
    return False

def get_user_groups_by_type(user: User, group_type):
    groups = []
    for group in group_type.objects:
        if user in group.participants:
            groups.append(group)
    return list(groups)

def create_new_group(name: str, description: str, participants: List[User], admins: List[User]) -> None:
    group = Group(name=name, description=description, participants=participants, admins=admins)
    group.save()