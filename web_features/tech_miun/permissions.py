MASTER_MIUN = 'גף מיון'
ESTIMATOR_MIUN = 'מעריך מיון'
BEHAVIORAL_DIAGNOSTICIAN_MIUN = 'מאבחנת מיון'
SAGAB_MIUN = 'סגב מיון'
ALL_MIUN_ROLES = [MASTER_MIUN, ESTIMATOR_MIUN, BEHAVIORAL_DIAGNOSTICIAN_MIUN, SAGAB_MIUN]


def is_master_miun(user):
    """
    :param user: User object
    :return: True if user is part of Gaf Miun
    """
    return MASTER_MIUN in user.role or True #TODO: change


def is_estimator_miun(user):
    """
    :param user: User object
    :return: True if user is an Estimator - "Ma'arich"
    """
    return ESTIMATOR_MIUN in user.role or True


def is_behavioral_diagnostician_miun(user):
    """
    :param user: User object
    :return: True if user is an Behavioral Diagnostician - "Me'avhenet"
    """
    return BEHAVIORAL_DIAGNOSTICIAN_MIUN in user.role or True


def is_sagab_miun(user):
    """
    :param user: User object
    :return: True if user is an interviewer - "Sagab"
    """
    return SAGAB_MIUN in user.role or True


def is_user_miun(user):
    """
    :param user: User object
    :return: True if user has any role in Miun
    """
    return any([role in user.role for role in ALL_MIUN_ROLES]) or True
