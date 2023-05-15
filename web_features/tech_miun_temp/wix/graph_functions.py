def plot(chartJsComponent, x, y, title):
    chartJsComponent.plot(x, y)
    chartJsComponent.title(title, size=30)


def bar(chartJsComponent, x, y, title):
    chartJsComponent.bar(x, y)
    chartJsComponent.title(title, size=30)


def radar(chartJsComponent, x, y, title):
    chartJsComponent.radar(x, y)
    chartJsComponent.title(title, size=30)


def scatter(chartJsComponent, x, y, title):
    chartJsComponent.scatter(x, y)
    chartJsComponent.title(title, size=30)


def pie(chartJsComponent, x, y, title):
    chartJsComponent.pie(x, y)
    chartJsComponent.title(title, size=30)


def doughnut(chartJsComponent, x, y, title):
    chartJsComponent.doughnut(x, y)
    chartJsComponent.title(title, size=30)

GRAPH_FUNCTIONS = {
    'plot': plot,
    'bar': bar,
    'radar': radar,
    'scatter': scatter,
    'pie': pie,
    'doughnut': doughnut,
}

