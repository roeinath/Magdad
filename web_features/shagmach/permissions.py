def is_user_admin(user):
    return user.name in ["יהלי אקשטיין", "עדי לוין", "אוראל ברק", "גיא דניאל הדס"] or 'תממ' in user.role


def is_user_rasap(user):
    return user.name in ["שחר דנק", "רון זכריה", "טל ברוקר",
                         "הראל מייל", "עומר רביב", "אורי בירנבוים",
                         "יהלי אקשטיין", "עדי לוין", "אוראל ברק", "גיא דניאל הדס"]


def is_user_medical_allowed(user):
    return user.name in ["יהלי אקשטיין", "תומר זילברמן", "גיא דניאל הדס"]


def is_user_food_allowed(user):
    return user.name in ["יהלי אקשטיין", "עדי לוין", "אוראל ברק", "גיא דניאל הדס", "אביב שמש"]
