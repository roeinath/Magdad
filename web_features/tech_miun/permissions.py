MASTER_MIUN = 'גף מיון'
ESTIMATOR_MIUN = 'מעריך מיון'
BEHAVIORAL_DIAGNOSTICIAN_MIUN = 'מאבחנת מיון'
SAGAB_MIUN = 'סגב מיון'
ALL_MIUN_ROLES = [MASTER_MIUN, ESTIMATOR_MIUN, BEHAVIORAL_DIAGNOSTICIAN_MIUN, SAGAB_MIUN]


def is_master_miun(user):
    return MASTER_MIUN in user.role


def is_estimator_miun(user):
    return ESTIMATOR_MIUN in user.role


def is_behavioral_diagnostician_miun(user):
    return BEHAVIORAL_DIAGNOSTICIAN_MIUN in user.role


def is_sagab_miun(user):
    return SAGAB_MIUN in user.role


def is_user_miun(user):
    return any([role in user.role for role in ALL_MIUN_ROLES])