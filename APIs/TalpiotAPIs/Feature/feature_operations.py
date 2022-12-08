from APIs.TalpiotAPIs.Feature.feature import Feature


def get_features():
    return Feature.objects


def get_features_by_category(user):
    """
    Get the features the user is allowed to use grouped by categories (in a dict)
    :param user:
    :return:
    """
    features = get_features()
    disallowed = []

    for feature in features:
        allowed = False
        for role in feature.authorized_roles:
            if role in user.role:
                allowed = True
        if 'admin' in user.role:
            allowed = True
        if not allowed:
            disallowed.append(feature)
    features = [feature for feature in features if feature not in disallowed]

    result = dict()
    for feature in features:
        if feature.category not in result:
            result[feature.category] = []
        result[feature.category].append(feature)
    return result
