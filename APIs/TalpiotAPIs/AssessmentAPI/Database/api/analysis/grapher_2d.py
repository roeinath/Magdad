import numpy as np

from APIs.TalpiotAPIs.AssessmentAPI.Database.api.pipeline import PipeLine


class Grapher(PipeLine):
    AVERAGE = lambda x: Grapher(x, x) + PipeLine(lambda a: a[2])
    MEDIAN = lambda x: Grapher(x, x) + PipeLine(lambda a: a[3])
    STDV = lambda x: Grapher(x, x) + PipeLine(lambda a: a[4])

    def __init__(self, x, y):
        PipeLine.__init__(self,
                          lambda prev: Grapher.preform_analysis(prev, x, y))

    @staticmethod
    def preform_analysis(prev, x, y):
        x_l = np.array([elem[x] for elem in prev])
        y_l = np.array([elem[y] for elem in prev])
        stdv = np.std(y_l)
        avg = np.average(y_l)
        median = np.median(y_l)
        return x_l, y_l, avg, median, stdv
