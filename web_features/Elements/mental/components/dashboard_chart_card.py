from web_features.Elements.mental.components.dashboard_card import DashboardCard
from web_framework.server_side.infastructure.components.chartjs_component import ChartjsComponent
from web_framework.server_side.infastructure.components.container import Container
from web_framework.server_side.infastructure.components.label import Label


class DashboardChartCard(DashboardCard):
    Y_GRID = False
    Y_MIN = 0
    GRID = 'origin'
    FILL = 'origin'
    CBIC_INTER_MODE = 'monotone'
    TENSION = 0.3
    MAINTN_ASPCT_RTIO = False
    IS_RESPONSIVE = True
    CHART_BORDER_COLOR = 'rgba(2, 86, 218, 0.81)'
    CHART_FILL_COLOR = 'rgba(2, 86, 218, 0.32)'

    def __init__(self, grid_end, grid_start, title, chart_type=ChartjsComponent.LINE, labels=[], data=[]):
        super().__init__(grid_end, grid_start, title)

        self.note_label = Label('הערה', italic=True)
        note_cont = Container(height='5%', margin='0 0 10px 0', justify_content='center',
                              orientation='row')
        note_cont.set_child(self.note_label)
        self.add_child(note_cont)
        self.chart = ChartjsComponent()
        self.chart_type = chart_type

        # apply chart options
        self.chart.set_option('responsive', self.IS_RESPONSIVE)
        self.chart.set_option('maintainAspectRatio', self.MAINTN_ASPCT_RTIO)
        self.chart.set_option('tension', self.TENSION)
        self.chart.set_option('cubicInterpolationMode', self.CBIC_INTER_MODE)
        self.chart.set_option('fill', self.FILL)
        self.chart.set_option('grid', self.GRID)
        self.chart.scale('y', min=self.Y_MIN, grid=self.Y_GRID)

        # determine chart type
        if self.chart_type == ChartjsComponent.LINE:
            self.chart.plot(x=labels, y=data, label=title, color=self.CHART_FILL_COLOR,
                            border_color=self.CHART_BORDER_COLOR)
        elif self.chart_type == ChartjsComponent.BAR:
            self.chart.bar(labels, data, label=self.title)
        elif self.chart_type == ChartjsComponent.doughnut:
            self.chart.doughnut(labels, data, label=self.title)

        chart_cont = Container(height='78%', padding=(0, 0, 0, 0),
                               margin=(0, 0, 0, 0))
        chart_cont.set_child(self.chart)
        self.add_child(chart_cont)

    def set_data(self, labels, data):
        self.chart.update_data(0, labels, data)

    def set_note(self, text, color='black'):
        self.note_label.update_text(text)
        self.note_label.update_color(fg_color=color)

    def remove_note(self):
        self.set_note(' ')
