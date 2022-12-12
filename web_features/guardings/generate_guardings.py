from mongoengine import Document, StringField, DateField

from APIs.TalpiotAPIs.Tasks.guarding.guarding_week import GuardingWeek
from APIs.TalpiotAPIs.Tasks.swap_request import SwapRequest
from APIs.TalpiotAPIs.User.user import User
from web_features.guardings import permissions
from APIs.TalpiotAPIs.mahzors_utils import *
from web_features.guardings.logic.generate_guardings.default_week_schedule_creator import create_week_default
from web_features.guardings.logic.generate_guardings.guarding_generator import generate_guardings
from web_framework.server_side.infastructure.actions import add_bot_command
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import HORIZONTAL, StackPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page

from web_features.guardings.view_guardings import DAY_LABEL_FORMAT, GUARDING_TIME_FORMAT


class GenerateGuardings(Page):
    def __init__(self, params):
        super().__init__()

        self.mahzor_selections = {}
        self.buttons_selections = {}

        self.sp = None
        self.popup = None
        self.week = None
        self.is_kaztar_selected = False

        self.send_to_guards_selected = False
        self.send_to_guards_btn: Button = None

        self.invite_guards_selected = False
        self.invite_guards_btn: Button = None

    @staticmethod
    def get_title() -> str:
        return "יצירת שמירות"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_guarding_admin(user)

    def get_page_ui(self, user):
        self.sp = StackPanel([])
        self.show_general_view()
        return self.sp

    def toggle_send_to_guards_select(self):
        if self.send_to_guards_selected:
            self.send_to_guards_selected = False
            self.send_to_guards_btn.update_color(bg_color='gray')
            self.send_to_guards_btn.update_color(fg_color='black')
            self.send_to_guards_btn.update_text("לא")
        else:
            self.send_to_guards_selected = True
            self.send_to_guards_btn.update_color(bg_color='green')
            self.send_to_guards_btn.update_color(fg_color='white')
            self.send_to_guards_btn.update_text("כן")

    def toggle_invite_guards_select(self):
        if self.invite_guards_selected:
            self.invite_guards_selected = False
            self.invite_guards_btn.update_color(bg_color='gray')
            self.invite_guards_btn.update_color(fg_color='black')
            self.invite_guards_btn.update_text("לא")
        else:
            self.invite_guards_selected = True
            self.invite_guards_btn.update_color(bg_color='green')
            self.invite_guards_btn.update_color(fg_color='white')
            self.invite_guards_btn.update_text("כן")

    def generate_guardings(self):
        for day in self.week.days:
            for task in day.guardings:
                if len(self.mahzor_selections[task]) == 0:
                    day.guardings.remove(task)
                    task.delete()
                    day.save()
        if generate_guardings(self.week, self.mahzor_selections, self.invite_guards_selected):
            self.sp.add_component(Label("סיימנו"))
            self.send_messages_to_guards(self.week)
        else:
            self.sp.add_component(Label("בעיה בשיבוץ, פנה לרמד talpix"))

    def send_messages_to_guards(self, week):
        text = ""
        if not self.send_to_guards_selected:
            text += "הודעה לא נשלחה לשומרים"
        else:
            for day in week.days:
                for task in day.guardings:
                    message_text = f"את/ה שומר/ת ב{get_hebrew_time(task.start_time)}"
                    add_bot_command("simple_send_message", {"user_list": task.assignment, "text": message_text})
            text += "הודעה נשלחה לשומרים"
        if self.invite_guards_selected:
            text += "\nשומרים זומנו בקלנדר"
        else:
            text += "\nשומרים לא זומנו בקלנדר"

        self.sp.add_component(Label(text))

    def show_week_generation_table(self, week_name, sunday):
        self.sp.clear()
        self.is_kaztar_selected = False

        self.sp.add_component(Label('שיבוץ שמירות עבור שבוע - ' + week_name, size=SIZE_EXTRA_LARGE))

        def on_kaztar_changed(new_kaztar_id):
            self.week.kaztar = User.objects(id=new_kaztar_id)[0]
            print("kaztar selected: ", reversed(str(self.week.kaztar)))
            self.is_kaztar_selected = True
            self.week.save()

        def mahzor_toggled(task, mahzor):
            """
            Toggles the mahzor's availability to take part in a given task, while updating the mahzor_button
            :param task:
            :param mahzor_button:
            :param mahzor:
            :return:
            """
            btn = self.buttons_selections[(task, mahzor)]
            if mahzor in self.mahzor_selections[task]:
                print(f"removed {mahzor} from {task}")
                btn.update_color(bg_color='Gray')
                self.mahzor_selections[task].remove(mahzor)
            else:
                print(f"added {mahzor} from {task}")
                btn.update_color(bg_color=get_mahzor_color(mahzor))
                self.mahzor_selections[task].append(mahzor)

        def mahzor_toggled_week(task_list, mahzor):
            """
            Toggles the mahzor's availability for the entire week.
            If the mahzor is available for at least one task, make it unavailable for all tasks
            otherwise, make it available to all tasks.
            :param task_list: the list of tasks for the day
            :param mahzor: the mahzor's number
            """
            if any((mahzor in self.mahzor_selections[task] for task in task_list)):  # mahzor is available for at least
                # one task
                for task in task_list:
                    if mahzor in self.mahzor_selections[task]:
                        mahzor_toggled(task, mahzor)
            else:  # mahzor unavailable for all tasks, make it available to all
                for task in task_list:
                    mahzor_toggled(task, mahzor)

        kaztar_sp = StackPanel([], orientation=HORIZONTAL)
        kaztar_sp.add_component(Label("בחר קצתר"))
        kaztar_options = {str(u.id): str(u.name) for u in User.objects(mahzor=get_mahzor_year_3().mahzor_num)}
        kaztar_sp.add_component(ComboBox(kaztar_options, on_kaztar_changed))
        self.sp.add_component(kaztar_sp)

        send_message_sp = StackPanel([], orientation=HORIZONTAL)
        send_message_sp.add_component(Label("שלח הודעה לשומרים"))
        self.send_to_guards_btn = Button("לא", self.toggle_send_to_guards_select, bg_color='gray')
        send_message_sp.add_component(self.send_to_guards_btn)
        self.sp.add_component(send_message_sp)

        calender_invite_sp = StackPanel([], orientation=HORIZONTAL)
        calender_invite_sp.add_component(Label("לזמן שומרים בקלנדר"))
        self.invite_guards_btn = Button("לא", self.toggle_invite_guards_select, bg_color='gray')
        calender_invite_sp.add_component(self.invite_guards_btn)
        self.sp.add_component(calender_invite_sp)

        self.sp.add_component(Button('חזור', self.show_general_view))

        table = GridPanel(20, 5, bg_color='talpiot_cyan')
        self.sp.add_component(table)

        def generate_or_err():
            if not self.is_kaztar_selected:
                self.sp.add_component(Label("שגיאה - יש לבחור קצתר", fg_color="red"))
            else:
                self.generate_guardings()

        generate = Button("שבץ", generate_or_err)
        self.sp.add_component(generate)

        self.week = create_week_default(sunday, week_name)

        for day_number, day in enumerate(self.week.days):
            day_column_ind = day_number

            day_title = DAY_LABEL_FORMAT.format(day_name=translate_day_name(day.date.strftime("%A")))
            day_header_stack = StackPanel([])
            day_header_stack.add_component(Label(day_title, fg_color='White', size=SIZE_MEDIUM))
            little_stack = StackPanel([], orientation=HORIZONTAL)
            day_header_stack.add_component(little_stack)

            for m in get_mahzors():
                btn = Button(text=m.short_name, bg_color=get_mahzor_color(m.mahzor_num), fg_color='black')
                btn.set_action(lambda key=m.mahzor_num, tasks=day.guardings:
                               mahzor_toggled_week(tasks, key))
                little_stack.add_component(btn)
            table.add_component(day_header_stack, 0, day_column_ind, 1, 1, bg_color=COLOR_PRIMARY_DARK)

            for i, task in enumerate(day.guardings):
                task_time = GUARDING_TIME_FORMAT.format(
                    day_name=translate_day_name(task.start_time.strftime("%A")),
                    start_time=task.start_time.strftime("%H:%M"),
                    end_time=task.end_time.strftime("%H:%M"))
                if task.task_type.description:
                    title_str = task_time + " ( " + task.task_type.description + ")"
                else:
                    title_str = task_time
                title = Label(title_str, size=SIZE_MEDIUM, fg_color='White')

                stack1 = StackPanel([])
                table.add_component(stack1, i + 1, day_column_ind, 1, 1)
                stack1.add_component(title)

                mahzors = StackPanel(orientation=HORIZONTAL)
                # populate mahzors that can take the tasks
                self.mahzor_selections[task] = []
                for m in get_mahzors():
                    self.mahzor_selections[task].append(m.mahzor_num)
                    btn = Button(text=m.short_name, bg_color=get_mahzor_color(m.mahzor_num), fg_color='black')
                    self.buttons_selections[(task, m.mahzor_num)] = btn
                    btn.set_action(lambda task=task, key=m.mahzor_num: mahzor_toggled(task, key))
                    mahzors.add_component(btn)
                stack1.add_component(mahzors)

    def delete_week(self, week):
        # Collect all the tasks from that week, to delete later. In the meanwhile delete the days and finally the week itself
        tasks_to_del = []
        for day in week.days:
            for task in day.guardings:
                tasks_to_del.append(task)
            day.delete()
        week.delete()

        # Delete the collected tasks
        for task in tasks_to_del:
            for req in SwapRequest.objects:
                if req.offer in tasks_to_del:
                    req.delete()
            task.delete()

        self.show_general_view()

    def show_general_view(self):
        self.sp.clear()

        def generate_new_week():
            class WeekGenerationForm(Document):
                week_name = StringField()
                date = DateField()

            form = JsonSchemaForm(WeekGenerationForm, visible=['week_name', 'date'], display_name={
                'week_name': 'שם השבוע',
                'date': 'יום ראשון',
            }, placeholder={
                'week_name': 'שבוע 0',
                'date': '0000-00-00',
            }, submit=lambda x: self.show_week_generation_table(x.week_name, x.date))

            self.popup = PopUp(form, title="יצירת שבוע", is_shown=True, is_cancelable=False)
            self.sp.add_component(self.popup)

        self.sp.add_component(Label('שיבוץ שמירות', size=SIZE_EXTRA_LARGE))

        self.sp.add_component(Button("+ צור שבוע", generate_new_week))

        self.sp.add_component(Label('שבועות קיימים', size=SIZE_LARGE))

        weeks = GuardingWeek.objects.all()

        weeks_grid = GridPanel(len(weeks), 4, bg_color='White')
        self.sp.add_component(weeks_grid)

        for i in range(len(weeks)):
            week = weeks[i]

            weeks_grid.add_component(Label(week.name, size=SIZE_MEDIUM), i, 0)
            weeks_grid.add_component(Button("מחק", lambda w=week: self.delete_week(w)), i, 2)
            weeks_grid.add_component(Button("שלח הודעות לשומרים", lambda w=week: self.send_messages_to_guards(w)), i, 3)
