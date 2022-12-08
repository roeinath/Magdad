from APIs.TalpiotAPIs.AssessmentAPI.Database.api.pipeline import PipeLine


class Sorter(PipeLine):

    def __init__(self, field, key=None):
        PipeLine.__init__(self, lambda prev: Sorter.do_sort(prev, field, key))

    @staticmethod
    def do_sort(prev, field, key):
        return sorted(prev, key=lambda a:
        a[field] if key is None else key(a[field])
                      )
