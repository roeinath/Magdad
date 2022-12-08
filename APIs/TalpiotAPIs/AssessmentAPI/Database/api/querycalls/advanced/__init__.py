from APIs.TalpiotAPIs.AssessmentAPI.Database.api.querycalls import Query
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.querycalls.filter import Filter

__empty_query = Query()


def get_talpions_by_affiliation(affiliation_query: Query):
    def get_applicable_talpions():
        # affils = affiliation_query.get_specific_field(Affiliation, "talpions")
        talps = [aff.talpions for aff in affils]
        talps_expanded = [talp for talp in talps][0]  # No idea why
        return [talp.id for talp in talps_expanded]

    return Filter.in_filter("_id", get_applicable_talpions)


def any_in_list_match_query(field: str, query: Query, my_database, list_database):
    def get_applicable_obj():
        legal_item = list(map(lambda a: a.id, query.get_specific_field(list_database, "id")))
        all_of_me = __empty_query.execute(my_database)
        rel_tuples = map(lambda a: (a.id, a[field]), all_of_me)
        tuples_filtered = filter(lambda t: any(map(lambda v: v.id in legal_item, t[1])), rel_tuples)
        return [tup[0] for tup in tuples_filtered]

    return Filter.in_filter("_id", get_applicable_obj)

