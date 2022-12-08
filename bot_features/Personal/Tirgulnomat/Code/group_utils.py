from APIs.TalpiotAPIs.Group import TeamGroup


# TODO: This is written stupidly.

def get_team_commander(user):
    a = list(filter(lambda x: user in x.participants, list(TeamGroup.objects())))
    if a:
        return a[0].commander
    return None


def get_subordinates_by_commander(user):
    a = list(filter(lambda x: user == x.commander, list(TeamGroup.objects())))
    if a:
        return a[0].participants
    return []


def get_division_commander(user):
    a = list(filter(lambda x: user in x.participants, list(TeamGroup.objects())))
    if a:
        return a[0].division.commander
    return None
