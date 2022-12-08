
def is_user_admin(user):
    return user.name in ['מדר תלפיות', "יהלי אקשטיין", "דוד אורן", "עדי לוין", "אלון בן דב", "רתם לפיד", "מפקד תלפיות",
                         "יסמין שאקי"]


def is_user_kamat(user):
    return is_user_admin(user)


def is_user_m_gaf_nihul(user):
    return user.name in ["אני מאיר"] or is_user_admin(user)


def is_user_talpiot_commander(user):
    return user.name in ["מפקד תלפיות"] or is_user_admin(user)


def is_user_pum_commander(user):
    return user.name in ["מפקד ביה\"ס"] or is_user_admin(user)


def is_user_permitted(user):
    return any(is_user(user) for is_user in [is_user_admin, is_user_kamat, is_user_m_gaf_nihul,
                                             is_user_talpiot_commander, is_user_pum_commander])
