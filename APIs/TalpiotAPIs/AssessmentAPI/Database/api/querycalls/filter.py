from APIs.TalpiotAPIs.AssessmentAPI.Database.api.querycalls.logical_filter import LogicalFilter
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.querycalls.query import Query


class Filter(Query):
    # ------------ PRIMITIVE FILTERS ------------
    """

    These filters apply only to primitive fields (i.e. not references or lists). When used on non-primitive types
    the behaviour of these filters is unpredictable (expect crashes).

    """

    @staticmethod
    def regex_filter(field, val):
        """
        :param field: the field this filter acts on. Has to be String field
        :param val: the regex that will be run on the field
        :return: a query that returns all objects whos field matches the regex
        """
        return Filter(field, "$regex", val)

    @staticmethod
    def greater_filter(field, val):
        """
        :param field: the field this filter acts on. Has to be number field
        :param val: the number that need to be less the the field number
        :return: a query that returns all objects whos field has a greater value than the given one
        """
        return Filter(field, "$gt", val)

    @staticmethod
    def lesser_filter(field, val):
        """
        :param field: the field this filter acts on. Has to be number field
        :param val: the number that need to be greater the the field number
        :return: a query that returns all objects whos field has a lower value than the given one
        """
        return Filter(field, "$lt", val)

    @staticmethod
    def in_filter(field, val):
        """
        This *might* work with non primitive objects, by checking if their ID is in the list,
        although it is prone to bugs.

        :param field: the field this filter acts on.
        :param val: The list that includes all legal options for this field
        :return: a query that returns all objects whos field has a legal value, as indicated in the provided list
        """
        return Filter(field, "$in", val)

    @staticmethod
    def has_field_filter(field):
        """
        :param field: the field that we want to exist
        :return: a query that returns all objects who have a field with the given name
        """
        return Filter(field, "$exists", True)

    @staticmethod
    def doesnt_have_field_filter(field):
        """
        :param field: the field that we want to not exist
        :return: a query that returns all objects who don't a field with the given name
        """
        return Filter(field, "$exists", False)

    @staticmethod
    def not_in_filter(field, val):
        """
        This *might* work with non primitive objects, by checking if their ID is in the list,
        although it is prone to bugs.

        :param field: the field this filter acts on.
        :param val: The list that includes all illegal options for this field
        :return: a query that returns all objects whos field has a legal value, as indicated in the provided list
        """
        return Filter(field, "$nin", val)

    @staticmethod
    def is_filter(field, val):
        """
        :param field: the field this filter acts on
        :param val: the value that we want the field to have
        :return: a query that returns all objects whos field has a value equal to the given one
        """
        return Filter(field, "$eq", val)

    @staticmethod
    def contains_filter(field, val):
        """
        :param field: the field this filter acts on. This field has to be a list of primitives
        :param val: the value which we want to appear in the array
        :return: a query that returns all objects whos field has an array, which contains the given value
        """
        return Filter(field, "$elemMatch", {"$eq": val})

    # ------------ PRIMITIVE FILTERS ------------

    @staticmethod
    def matches_query(field, query, db):
        """
        :param field: The field this query will test
        :param query: The query that will be run on the given field
        :param db: The document type of the field that is being tested

        :return: The query that returns all objects whos `field` matches the given `query` and is of type `db`
        """
        return Filter(field, "$in",
                      lambda: [match["id"]
                               for match in
                               query.get_specific_field(db, "id")])

    # TODO, test this sometimes
    # @staticmethod
    # def any_filter(field, query, db):
    #     return Filter(field, "$elemMatch",
    #                   {"$in": lambda: [match["id"]
    #                                    for match in
    #                                    query.get_specific_field(db, "id")]}
    #                   )

    def __init__(self, field: str, filter_type: str, filter_val):
        self.field = field
        self.filter_type = filter_type
        self.filter_val = filter_val
        Query.__init__(self, {field: {filter_type: filter_val}})

    def __add__(self, other):
        prev_q = other.query
        if self.field in prev_q:
            if type(prev_q) is not dict:
                raise Exception("Can't apply general "
                                "filter to exact match filter")
            if self.filter_type in prev_q[self.field]:
                raise Exception(self.filter_type +
                                " filter can only be applied once! Use `&` instead of `+`")
            prev_q[self.field][self.filter_type] = self.filter_val
        else:
            prev_q[self.field] = {self.filter_type: self.filter_val}

        return Query(prev_q, other.filters)

    def __or__(self, other):
        return LogicalFilter.OR(self, other)

    def __and__(self, other):
        return LogicalFilter.AND(self, other)

    def __invert__(self):
        return LogicalFilter.NOT(self)
