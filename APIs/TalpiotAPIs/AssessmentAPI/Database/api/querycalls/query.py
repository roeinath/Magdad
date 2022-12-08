
class Query:
    """
    This object represents a query on the database.
    Adding queries to each other is essentially like putting an 'and' operator between them, i.e. only object that
    match both queries will be returned. You can also use bitwise operators to combine queries (as if they were logical
    operators. e.g.
        either_or = query1 | query2
        all_that_dont_match = ~ query1
        matching_both = query1 & query2
    Note that `query1 & query2` is equivalent (mostly) to `query1 + query2`.
    """
    LOGICAL_FILTERS = ["$or", "$and"]

    def __init__(self, quer=None, filt=None):
        self.query = quer if quer is not None else {}
        self.filters = filt if filt is not None else {}

    def execute(self, document):
        """
        :return: All objects that are saved in a given document, that match this query.
        """
        return document.objects(__raw__=Query.finalize_query(self.query))

    def get_specific_field(self, document, field):
        """
        :return: The fields of the the objects in the given document that match the query. \
            note that this will be returned in the following format: \
                [{"field_name": field_val1}, {"field_name": field_val2} ...] \
            and not as: \
                [field_val1, field_val2 ...]
        """
        return document.objects(__raw__=Query.finalize_query(self.query)).only(
            field)

    @staticmethod
    def finalize_query(query):
        new_query = {}
        for key in query:
            tp = type(query[key])
            if tp is dict:
                new_query[key] = Query.finalize_query(query[key])
            elif callable(query[key]):
                new_query[key] = query[key]()
            elif key in Query.LOGICAL_FILTERS:
                new_query[key] = [Query.finalize_query(elem) for elem in
                                  query[key]]
            else:
                new_query[key] = query[key]
        return new_query

    def __str__(self):
        return str(Query.finalize_query(self.query))
