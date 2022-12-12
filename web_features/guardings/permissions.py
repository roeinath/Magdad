def is_user_guarding_admin(user):
    return user.name in ["ירדן גלפן", "אייל צווכר", "רפאל קלוטניק", "יהלי אקשטיין", "עדי לוין", "אוראל ברק"]


def is_user_guarding_super_admin(user):
    # those users have permissions to view guarding exemptions.
    # Only sagaz can be here (צנעת הפרט).
    return user.name in ["ירדן גלפן", "גיא כרמלי", "יהלי אקשטיין", "עדי לוין"]
