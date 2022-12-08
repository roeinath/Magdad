from fuzzywuzzy import fuzz


def query_similar_objects(collection_class=None, from_objects: list = None, limit_objects: int = -1, **query_args) -> list:
    """
    Queries non-exact values of fields.

    Example:
        query_similar_objects(collection_class=User, name='יהלי') -> ['יהלי אקשטיין', 'יהלי קדמן', ...]
        query_similar_objects(collection_class=User, name='יהלי', limit_objects=1) -> ['יהלי אקשטיין']
        query_similar_objects(from_objects=User.objects(mahzor=42), name='יהלי') -> ['יהלי אקשטיין', 'יהלי קדמן', ...]


    :return: A list of all objects, sorted by the similarity of a field to a value
    :param collection_class: The class of the collection (for example: User, Task, ...)
    :param from_objects: optional parameter. if not None, take those objects and sorts them by similarity.
                                            if None, get all objects from the collection
    :param limit_objects: Limit the number of return objects
    :param query_args: the query arguments, a dictionary of fields name and value.
    """
    if collection_class is None and from_objects is None:
        return []

    from_objects = list(collection_class.objects) if from_objects is None else from_objects
    ratios = [(1, object_) for object_ in from_objects]
    for field_name, value in query_args.items():
        try:
            ratios = [(fuzz.token_set_ratio(value, getattr(object_, field_name)) * ratio, object_)
                      for ratio, object_ in ratios]
        except AttributeError:
            print(f"Error in query_similar_objects: could not find field named {field_name}")
    ratios.sort(key=lambda x: x[0], reverse=True)
    return [object_ for ratio, object_ in ratios][:limit_objects]
