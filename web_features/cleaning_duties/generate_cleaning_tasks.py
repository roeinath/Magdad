from mongoengine import Document, StringField, DateField

from APIs.TalpiotAPIs.CleaningTasks.cleaning.cleaning_week import CleaningWeek
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.mahzors_utils import *
from web_features.cleaning_duties import permissions
from web_features.cleaning_duties.logic.generate_cleaning_tasks.cleaning_generator import generate_cleanings
from web_features.cleaning_duties.logic.generate_cleaning_tasks.default_week_schedule_creator import create_week_default
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import HORIZONTAL, StackPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page


def delete_week(week):
    tasks_to_del = []
    for day in week.days:
        for task in day.cleaning_duties:
            tasks_to_del.append(task)
        day.delete()
    week.delete()


class GenerateCleaningTasks(Page):
    def __init__(self, params):
        super().__init__()

        self.sp = None
        self.popup = None
        self.week = None
        self.mahzor_selections = {}

    @staticmethod
    def get_title() -> str:
        return "יצירת תורנות"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_cleaning_task_admin(user)

    def on_select(self, task, mahzor):
        # self.sp.add_component(Label(str(task)))
        self.mahzor_selections[task] = mahzor

    def generate_cleaning_tasks(self):

        generate_cleanings(self.week)

        self.sp.add_component(Label("סיימנו"))

    def show_generate_week_view(self, week: CleaningWeek):
        pass

    class Test(Document):
        week_name = StringField()
        date = DateField()

    def mahzor_toggled(self, task, mahzor_button, mahzor):
        if mahzor in self.mahzor_selections[task]:
            print(f"removed {mahzor} from {task}")
            mahzor_button.update_color(bg_color='Gray')
            self.mahzor_selections[task].remove(mahzor)
        else:
            print(f"added {mahzor} from {task}")
            mahzor_button.update_color(bg_color=get_mahzor_color(mahzor))
            self.mahzor_selections[task].append(mahzor)

    def got_new_week_name(self, week_name, sunday):
        print("Got the weekname", week_name)

        # self.popup.hide()
        self.sp.clear()

        self.sp.add_component(Label('שיבוץ תורנות עבור שבוע - ' + week_name, size=SIZE_EXTRA_LARGE))

        def on_a_mishmahat_changed(new_a_mishmahat_id):
            self.week.a_mishmahat = User.objects(id=new_a_mishmahat_id)[0]
            print("A' mishmahat selected: ", reversed(str(self.week.a_mishmahat)))
            self.week.save()

        a_mishmahat_sp = StackPanel([], orientation=HORIZONTAL)
        a_mishmahat_sp.add_component(Label("בחר א משמעת"))
        a_mishmahat_options = {str(u.id): str(u.name) for u in User.objects(mahzor=get_mahzor_year_3().mahzor_num)}
        a_mishmahat_sp.add_component(ComboBox(a_mishmahat_options, on_a_mishmahat_changed))
        self.sp.add_component(a_mishmahat_sp)

        self.sp.add_component(Button('חזור', self.show_general_view))

        tables = [GridPanel(20, 5, bg_color='talpiot_cyan') for i in range(3)]
        for table in tables:
            self.sp.add_component(table)
        generate = Button("שבץ", self.generate_cleaning_tasks)
        self.sp.add_component(generate)

        # TODO: Add sunday
        self.week = create_week_default(sunday, week_name)

        year_3 = get_mahzor_year_3().mahzor_num

        for day_number, day in enumerate(self.week.days):
            day_column_ind = day_number

            num_added_to_table = {t: 1 for t in tables}

            day_of_week_name = day_of_week_num_to_hebrew_name(day.date.weekday())
            for table in tables:
                table.add_component(
                    Label(day_of_week_name + ", " + str(len(day.cleaning_duties)), fg_color='White', size=SIZE_MEDIUM),
                    0, day_column_ind, 1, 1)
            for i, task in enumerate(day.cleaning_duties):
                stack1 = StackPanel([])
                if task.mahzor - year_3 < 0:
                    raise Exception("Invalid mahzor for cleaning task (not in current matlam)")

                table = tables[task.mahzor - year_3]
                title_str = task.start_time.strftime("%H:%M") + " עד " + task.end_time.strftime(
                    "%H:%M")
                title = Label(title_str, size=SIZE_MEDIUM, fg_color='White')
                stack1.add_component(title)

                # selection = ComboBox(get_mahzor_names(), lambda mahzor, task_t=task: self.on_select(task_t, int(mahzor)))
                mahzors = StackPanel(orientation=HORIZONTAL)
                btn = Button(task.mahzor, #action=lambda m=task.mahzor, t=task: self.on_select(t, m),
                             bg_color=get_mahzor_color(task.mahzor), fg_color='black')
                mahzors.add_component(btn)
                stack1.add_component(mahzors)

                table.add_component(stack1, num_added_to_table[table], day_column_ind, 1, 1)
                num_added_to_table[table] += 1

            max_tasks_per_day = 3
            for t in tables:
                while num_added_to_table[t] < max_tasks_per_day + 1:
                    t.add_component(Label(""), num_added_to_table[t], day_column_ind, 1, 1)
                    num_added_to_table[t] += 1

        # stack = StackPanel([title, selection], orientation=VERTICAL)

    def generate_new_week(self):

        form = JsonSchemaForm(GenerateCleaningTasks.Test, visible=['week_name', 'date'], display_name={
            'week_name': 'שם השבוע',
            'date': 'יום ראשון',
        }, placeholder={
            'week_name': 'שבוע 0',
            'date': '0000-00-00',
        }, submit=lambda x: self.got_new_week_name(x.week_name, x.date))

        # self.sp.add_component(form)

        self.popup = PopUp(form, title="יצירת שבוע", is_shown=True, is_cancelable=False)
        self.sp.add_component(self.popup)

    def show_general_view(self):
        self.sp.clear()

        self.sp.add_component(Label('שיבוץ תורנויות', size=SIZE_EXTRA_LARGE))

        self.sp.add_component(Button("+ צור שבוע", self.generate_new_week))

        self.sp.add_component(Label('שבועות קיימים', size=SIZE_LARGE))

        weeks = CleaningWeek.objects

        weeks_grid = GridPanel(len(weeks), 3, bg_color='White')
        self.sp.add_component(weeks_grid)

        for i in range(len(weeks)):
            week = weeks[i]

            weeks_grid.add_component(Label(week.name, size=SIZE_MEDIUM), i, 0)
            weeks_grid.add_component(Button("ערוך", lambda w=week: self.show_generate_week_view(w)), i, 1)
            weeks_grid.add_component(Button("מחק", lambda w=week: delete_week(w)), i, 2)

    def get_page_ui(self, user):
        self.sp = StackPanel([])

        self.show_general_view()

        return self.sp
