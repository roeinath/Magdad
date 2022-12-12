from typing import Dict, Iterable, Callable, List


def __group_by(lst: Iterable, key: Callable[[any], any]) -> Dict:
    """
    Groups the given iterable object by the given key
    :param lst: The source object
    :param key: The key to group by
    :return: A set of objects grouped by the key
    """
    # Create a set of the different keys
    keys = {key(item) for item in lst}
    keys_lst = list(keys)

    # Create a list of empty lists (groups) for each key
    grouped_set = {}

    # Iterate through the given set and add them to the grouped set
    for item in lst:
        item_key = key(item)

        if item_key not in grouped_set:
            grouped_set[item_key] = []

        grouped_set[item_key].append(item)

    return grouped_set


def __get_nested_key(dic: Dict, keys: List, default_val=None) -> any:
    data = dic
    for key in keys:
        try:
            data = data.get(key, None)
            if data is None:
                return default_val
        except:
            return None

    return data


def manipulate(data: Dict, group_by: List[str] = None, sort_groups=False, sort_by: List[str] = None, filters=None):
    if filters is None:
        filters = []

    result = data
    if group_by is not None:
        result = __group_by(data, lambda sub: __get_nested_key(sub, group_by))

        if sort_groups:
            result = list(map(lambda k, v: v, sorted(result.items(), key=lambda k, v: k)))
        else:
            result = list(result.values())

        if sort_by is not None:
            result = list(
                map(lambda group: list(sorted(group, key=lambda item: __get_nested_key(item, sort_by))), result))

        for fil, val in filters:
            # Filter items inside groups
            result = list(map(lambda group: list(filter(lambda item: __get_nested_key(item, fil, None) == val, group)),
                              result))
            # Remove empty groups
            result = list(filter(lambda group: len(group) > 0, result))
    elif sort_by is not None:
        result = list(sorted(data, key=lambda item: __get_nested_key(item, sort_by)))

        for fil, val in filters:
            result = list(filter(lambda item: __get_nested_key(item, fil, None) == val, result))

    return result
