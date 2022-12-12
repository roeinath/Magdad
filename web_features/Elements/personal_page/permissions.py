from APIs.TalpiotAPIs.AssessmentAPI.Database.api.getdata.academy_grades_interface import *
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.getdata.skirot_grades_interface import *
from web_features.Elements.personal_page.modules.constants import *


def is_user_X_admin(user):
    return user.name in ["יהלי אקשטיין", "יואב פלטו" ,"מישל זילבר", "יובל פישמן"]


def is_group_data_authorized(user):
    """
    checks whether user have permission to see group data
    :param user:  user object
    :return: true iff user can see group data
    """
    if user.name in GROUP_DATA_AUTHORIZED:
        return True
    return False


def is_user_captain(user):
    return user.name in ["רועי גרנות", "זיו ליברמן", "מדר תלפיות", "צליל ברבי", "יותם סלעי",
                         "גיל בועזי", "נדב נפתלי", "שקד רייך", "עדי אשר", 
                         "אלון וולף", "אלעד קליגר", "רועי מזרחי", "רועי סמואלס"]


def is_user_sagaz(user):
    return user.mahzor == CURRENT_SAGAZ


def is_user_cadet(user):
    return not is_user_captain(user)


def is_user_have_permissions(using_user, wanted_user):
    """
    checks whether using_user have permissions to see wanted_user data
    :param using_user:  user object
    :param wanted_user: string/user object
    :return: true iff using_user can see wanted_user data
    """
    # each user can see himself
    wanted_user_name = wanted_user
    if type(wanted_user) != str:
        wanted_user_name = wanted_user.name
    using_user_name = using_user.name

    if using_user_name == wanted_user_name:
        return True

    # captain have permission for all
    if is_user_captain(using_user):
        return True

    if is_user_sagaz(using_user):
        team = get_team_of_sagaz(using_user)
        names = [u.name for u in team]
        if len(names) != 0:
            if wanted_user_name in names:
                return True

        # if in relevant role
        if is_group_data_authorized(using_user):
            return True

    if is_user_X_admin(using_user):
        return True

    return False

# if __name__ == "__main__":
#     set_up_DB()
#     noam = get_user_by_name("נועם שקד כהן")
#     ivri = get_user_by_name("עידו עברי")
#     is_user_have_permissions(noam, ivri)
