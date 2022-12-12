from dataclasses import dataclass
from statistics import mean
from typing import Tuple, List, Dict

import web_framework.server_side.infastructure.constants as const
from APIs.TalpiotAPIs import User, NewForm, FormSubmission, FloatQuestion, IntegerQuestion, TextQuestion, Question
from APIs.TalpiotAPIs.Mental import TrackedMentalData
from APIs.Tools.DataManipulation import dictionary
from web_features.Elements.mental.components.add_data_card import AddDataCard
from web_features.Elements.mental.components.dashboard_card import DashboardCard
from web_features.Elements.mental.components.dashboard_chart_card import DashboardChartCard
from web_features.Elements.mental.permissions import MentalDashboardPermissions as perms
from web_framework.server_side.infastructure.components.card import Card
from web_framework.server_side.infastructure.components.chartjs_component import ChartjsComponent
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.components.grid_view import GridView
from web_framework.server_side.infastructure.components.json_schema_newform import JsonSchemaNewForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.page import Page

# Some constants
PAGE_TITLE = 'דשבורד מנטלי'

MAX_GRID_WIDTH: 3
ONE_UNIT_HEIGHT: 45


@dataclass
class ChartData:
    name: str
    data: Tuple[List[any], List[any]]


@dataclass
class DashboardChart:
    title: str
    chartData: ChartData
    position: Tuple[Tuple[int, int], Tuple[int, int]]
    type: str

    def height(self):
        return self.position[1][1] - self.position[0][1]


class MentalDashboardPage(Page):
    def __init__(self, params):
        super().__init__(params)
        self._parsed_chart_data = {}
        self._filters_ui: JsonSchemaNewForm = None
        self._filters = {}
        self._grid_view: GridView = None
        self._charts: Dict[str, DashboardChartCard] = {}

        self._fixed_grid: List[list] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self._grid_sample: List[list] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        self._available_filters = {}

        self._chart_configurations: Dict[str, DashboardChart] = {}
        self._charts_raw_data = {}
        self._tracked_data_lst: Dict[str, TrackedMentalData] = {}
        self._forms = {}

    @staticmethod
    def get_title() -> str:
        return PAGE_TITLE

    @staticmethod
    def get_grid_size(charts: List[DashboardChart]) -> Tuple[int, int]:
        height = 0
        width = 0
        for chart in charts:
            width = max(chart.position[1][0], width)
            height = max(chart.position[1][1], height)

        return width, height

    def add_data_card(self, grid_start: Tuple[int, int], grid_end: Tuple[int, int]) -> Card:
        """
        Creates an admin card (which allows the user to add/edit/remove data)
        :param grid_start: Where will it start on the grid
        :param grid_end: Where will it end on the grid
        :return: The card itself
        """

        def add_data(data):
            forms = NewForm.objects(form_identifier=data["selectedChart"])
            assert forms is not None, f'Form {data["selectedChart"]} does not exist for some reason'

            assert len(forms) <= 1, 'More then one form?'

            for form in forms:
                form_submission = FormSubmission()
                form_submission.form = form

                for field in form.fields:
                    if isinstance(field, Question):
                        question: Question = field

                        answer = question.new_answer()
                        answer.question = question
                        answer.set_value(question.get_answer_type()(data[question.field_identifier]))

                        answer.save()
                        form_submission.answers.append(answer)

                form_submission.save()

                # Update the chart
                self.fetch_data()
                self.make_charts()

                new_data = self._chart_configurations[form.form_identifier].chartData
                self._charts[form.form_identifier].set_data(0, *new_data.data)

        card = DashboardCard(grid_start, grid_end, 'הוספת נתון')

        form = NewForm()
        form.form_identifier = 'newDataForm'

        form_question = TextQuestion()
        form_question.field_identifier = 'value'
        form_question.question = 'הכנס נתון'

        form_question1 = TextQuestion()
        form_question1.field_identifier = 'selectedChart'
        form_question1.question = 'בחר נתון רצוי'
        form_question1.set_options(
            {trkd_dat.name: trkd_dat.identifier for trkd_dat in self._tracked_data_lst.values()})

        form_question2 = IntegerQuestion()
        form_question2.field_identifier = 'week'
        form_question2.question = 'שבוע'

        form_question3 = TextQuestion()
        form_question3.field_identifier = 'machzor'
        form_question3.question = 'מחזור'
        form_question3.set_options({
            'מ"ד': 'מ"ד',
            'מ"ב': 'מ"ב',
            'מ"ג': 'מ"ג'
        })

        form.fields = [form_question1, form_question, form_question2, form_question3]

        form_ui = JsonSchemaNewForm(
            form,
            visible=['selectedChart', 'value', 'week', 'machzor'],
            display_name={'value': 'הכנס נתון',
                          'selectedChart': 'בחר נתון',
                          'week': 'שבוע', 'machzor': 'מחזור'},
            placeholder={'value': '...', 'week': '1'},
            value={'selectedChart': 'בחר...'},
            submit=add_data
        )

        card.add_child(form_ui)
        return card

    @staticmethod
    def create_data_category_card(grid_start: Tuple[int, int], grid_end: Tuple[int, int]):
        def add_data_category(data):
            print(f'Adding category: {data}')
            form = NewForm()
            form.form_identifier = data['categoryIdentifier']
            form.name = data['categoryName']

            value_ques = FloatQuestion()
            value_ques.field_identifier = 'value'
            value_ques.question = data['categoryName']
            value_ques.required = True

            value_ques.save()

            week_ques = IntegerQuestion()
            week_ques.field_identifier = 'week'
            week_ques.question = data['categoryName']
            week_ques.required = True

            week_ques.save()

            machzor_ques = TextQuestion()
            machzor_ques.field_identifier = 'machzor'
            machzor_ques.question = data['categoryName']
            machzor_ques.required = True

            machzor_ques.save()

            form.fields = [value_ques, week_ques, machzor_ques]
            form.save()

            tracked_data = TrackedMentalData()
            tracked_data.form = form
            tracked_data.name = data['categoryName']
            tracked_data.identifier = data['categoryIdentifier']

            tracked_data.save()

        card = Card(height=f'{45 * (grid_end[1] - grid_start[1])}vh', padding=15, corner_radius=2, bg_color='white',
                    grid_start=grid_start,
                    grid_end=grid_end)
        card.apply_shadow(x_off=2, y_off=4, blur=9, spread=3, color='black', opacity=.1)

        sp = StackPanel()
        form = NewForm()
        form.form_identifier = 'addDataCategory'

        form.fields = {
            TextQuestion(
                field_identifier='categoryName',
                question='שם הנתון?',
            ),
            TextQuestion(
                field_identifier='categoryIdentifier',
                question='מזהה',
            )
        }

        form_ui = JsonSchemaNewForm(
            form_doc=form,
            visible=['categoryName', 'categoryIdentifier'],
            display_name={
                'categoryName': 'שם הנתון',
                'categoryIdentifier': 'מזהה הנתון'
            },
            submit=add_data_category
        )

        card.title('יצירת נתון', bold=True, size=const.SIZE_MEDIUM)
        card.add_child(form_ui)

        return card

    def create_filters_card(self, filters, filter_results):
        title_card = DashboardCard((3, 1), (4, 2), 'דשבורד מנטלי 🎛')
        #     self.dashboard_card((3, 1), (4, 2))
        # title_card.title(PAGE_TITLE, size=const.SIZE_EXTRA_LARGE, bold=True, align='right')
        title_card.add_child(Label('פילטרים', size=const.SIZE_MEDIUM, bold=True))

        # TODO: get the list from submissions
        machzor_filter = ComboBox({
            'מ"ד': 'מ"ד',
            'מ"ג': 'מ"ג',
            'מ"ב': 'מ"ב',
            '*': 'כולם',
        }, lambda selection: filter_results('machzor', selection), '*')

        machzor_filter_sp = StackPanel(orientation=const.HORIZONTAL)
        machzor_filter_sp.add_component(Label('מחזור'))
        machzor_filter_sp.add_component(machzor_filter)

        self._filters_ui = machzor_filter_sp

        title_card.add_child(machzor_filter_sp)
        return title_card

    def set_filter(self, fil, val):
        if val == '*':
            if self._filters.get(fil) is not None:
                self._filters.pop(fil)
        else:
            self._filters[fil] = val

        self.parse_data()
        self.make_charts()
        self.update_charts()

    def add_chart(self, identifier, dashboard_chart):
        # check for overlapping
        for i in range(dashboard_chart.position[0][0] - 1, dashboard_chart.position[1][0] - 1):
            for j in range(dashboard_chart.position[0][1] - 1, dashboard_chart.position[1][1] - 1):
                # self.grid_sample[i][j] += 1
                if self._grid_sample[i][j] > 1:
                    return False

        card = DashboardChartCard(dashboard_chart.position[0], dashboard_chart.position[1], title=dashboard_chart.title,
                                  labels=dashboard_chart.chartData.data[0], data=dashboard_chart.chartData.data)

        self._grid_view.add_component(card)
        self._charts[identifier] = card
        return True

    def init_grid(self):
        grid_size = (3, 3)
        self._grid_sample = [[self._fixed_grid[row][col] for col in range(grid_size[0])] for row in range(grid_size[1])]

    def parse_data(self):
        # TODO: make the key a variable
        self._parsed_chart_data.clear()
        for chart_data_k in self._charts_raw_data:
            data_groups = dictionary.manipulate(self._charts_raw_data[chart_data_k], group_by=['answers', 'week'],
                                                filters=list(
                                                    map(lambda v: (['answers', v[0]], v[1]),
                                                        list(self._filters.items())))
                                                )
            for data_group in data_groups:
                # Calculate avgs
                avg = mean([data['answers']['value'] for data in data_group])

                if self._parsed_chart_data.get(chart_data_k, None) is None:
                    self._parsed_chart_data[chart_data_k] = []
                self._parsed_chart_data[chart_data_k].append((data_group[0]['answers']['week'], avg))

        print(self._parsed_chart_data)

    def fetch_data(self):
        tracked_datas: List[TrackedMentalData] = TrackedMentalData.objects()  # Fetch new data from database

        # Contains the by tracked-data, grouped by week (for now) and sorted
        parsed_data: Dict[str, Dict] = {}

        self._tracked_data_lst.clear()
        self._forms.clear()
        # Get all the forms to look for data in and their submissions
        for tracked_data in tracked_datas:
            self._tracked_data_lst[tracked_data.identifier] = tracked_data
            # Get form
            form = tracked_data.form
            self._charts_raw_data[form.form_identifier] = form.get_submissions()
            self._forms[tracked_data.identifier] = form

    def make_charts(self):
        self.init_grid()
        self._chart_configurations.clear()
        for data_id, data_entry in self._parsed_chart_data.items():
            chart_labels = []
            chart_data = []
            for lab, dat in data_entry:
                chart_labels.append(lab)
                chart_data.append(dat)

            # add to the dashboard
            x, y = self.find_next_empty()
            self._chart_configurations[data_id] = DashboardChart(
                chartData=ChartData(name=data_id, data=(chart_labels, chart_data)),
                position=((x, y), (x + 1, y + 1)), type=ChartjsComponent.LINE,
                title=self._tracked_data_lst[data_id].name)

    def find_next_empty(self) -> Tuple[int, int]:
        for i in range(len(self._grid_sample[0])):
            for j in range(len(self._grid_sample)):
                if self._grid_sample[j][i] == 0:
                    self._grid_sample[j][i] += 1
                    return (j + 1), (i + 1)

        return None

    def refresh_data(self):
        self._chart_configurations = {}
        self.fetch_data()
        self.parse_data()

    def update_charts(self):
        for chart_id, dashboard_card in self._charts.items():
            new_data = self._chart_configurations.get(chart_id, None)
            if new_data is not None:
                dashboard_card.set_data(*new_data.chartData.data)
                dashboard_card.remove_note()
            else:
                dashboard_card.set_data([], [])
                dashboard_card.set_note('חסרים נתונים', 'red')

    def get_page_ui(self, user: User):
        self.refresh_data()
        # TODO: Should determine grid size
        self._grid_view = GridView(3, 3, col_gap=12, row_gap=20, padding=20,
                                   max_width='100vw')

        title_card = self.create_filters_card(None, self.set_filter)

        self._fixed_grid[2][0] = 1

        # print(dict(map(lambda k: (k, self._parsed_chart_data[k].title), self._parsed_chart_data)).__repr__())

        data_card = AddDataCard((3, 2), (4, 4),
                                {trkd_dat.identifier: trkd_dat.name for trkd_dat in self._tracked_data_lst.values()}, self._forms)

        if perms.is_user_admin(user):
            # Show also the editing card
            self._grid_view.add_component(data_card)  # self.add_data_card((3, 2), (4, 4)))
            # self._grid_view.add_component(self.create_data_category_card((2, 2), (3, 3)))
            # self._gri d_sample[2][1] = 1
            self._fixed_grid[2][1] = 1
            pass

        self.init_grid()

        self._grid_view.add_component(title_card)
        self.make_charts()

        # Add the charts
        for ident, chart in self._chart_configurations.items():
            if not self.add_chart(ident, chart):
                self._grid_view.clear()
                # TODO: there is a bug here? wont load the page if label is returned
                return Label('Error: Overlapping charts', fg_color='red')

        self.update_charts()

        return self._grid_view
