from APIs.TalpiotAPIs.AssessmentAPI.Database.api.querycalls.query import Query


class LogicalFilter:
    OR = lambda f, s: LogicalFilter.execute_filter("$or", f, s)
    AND = lambda f, s: LogicalFilter.execute_filter("$and", f, s)
    NOT = lambda f: LogicalFilter.execute_filter("$not", f)

    @staticmethod
    def execute_filter(operator, first, second=None):
        if second is not None:
            if len(first.filters) + len(second.filters):
                raise Exception("Can't or expressions "
                                "that have black/whitelists")
            return Query({operator: [first.query, second.query]})
        else:
            if len(first.filters):
                raise Exception(
                    "Can't or expressions that have black/whitelists")
            return Query({operator: first.query})
