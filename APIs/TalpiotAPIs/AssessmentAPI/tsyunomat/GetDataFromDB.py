from APIs.TalpiotAPIs.AssessmentAPI.Database.login_info import LoginInfo


def get_users_info(madar_password):
    '''
    getting the login_info to a dict that the key is the cadet's name and value is
    a dict with 2 elements. first email and second password
    :return:
    '''

    users_info = LoginInfo.objects.filter().select_related(1)
    users_data = {}
    for info in users_info:
        users_data[info.user.name] = {'mahzor': info.user.mahzor,
                                      'email': LoginInfo.decrypt(madar_password, info.email),
                                      'password': LoginInfo.decrypt(madar_password, info.password),
                                      'cse_username': LoginInfo.decrypt(madar_password, info.cse_username),
                                      'cse_password': LoginInfo.decrypt(madar_password, info.cse_password)}
    return users_data


def get_specific_user_info(user_name):
    dict_all_users = get_users_info("elements")
    if user_name in dict_all_users:
        return dict_all_users[user_name]
    else:
        return None


