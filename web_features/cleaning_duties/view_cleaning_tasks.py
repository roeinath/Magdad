
from mongoengine import *

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.CleaningTasks.cleaning.cleaning_week import CleaningWeek
from APIs.TalpiotAPIs.CleaningTasks.cleaning_task import CleaningTask
from APIs.TalpiotAPIs.mahzors_utils import *
from APIs.TalpiotAPIs.static_fields import get_mahzor_number_list
from web_features.cleaning_duties import permissions
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.actions import simple_send_message
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel, VERTICAL, HORIZONTAL
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page



class CleaningSwap(Document):
    target: User = ReferenceField(User)
    one_sided: bool = BooleanField()
    own_task = ReferenceField(CleaningTask)


class SelfCleaningSwap(Document):
    target: User = ReferenceField(User)


def get_current_cleaning_week():
    x = CleaningWeek.objects(first_date=str(get_current_sunday()))
    if x:
        return x[0]
    weeks = CleaningWeek.objects()
    if len(weeks) == 0:
        return None
    else:
        return weeks[len(weeks) - 1]


def get_weeks_dict():
    res = {}
    for week in CleaningWeek.objects():
        print(str(week.id))
        print(week.name)
        res[str(week.id)] = week.name
    return res


class ViewCleaningTasks(Page):
    @staticmethod
    def get_title() -> str:
        return "הצגת תורנויות"

    def __init__(self, params):
        super().__init__()
        self.container_table = None
        self.popup = None

        self.is_edit_possible = False
        self.is_edit = False
        self.is_screenshot_mode = False
        self.last_selected_week = None
        self.additional_table = None
        self.a_mishmahat = None

        self.user = None

    class EditTask(Document):
        assigment = ListField(ReferenceField(User))

    def execute_swap(self, swap, curr_week_id, target_task: CleaningTask, owner: User):
        print("=======" + str(target_task.assignment))
        if swap.one_sided:
            target_task.assignment.remove(swap.target)
            target_task.assignment.append(owner)
            target_task.update_calendar_invite()
            target_task.save()
        else:
            if swap.target == None or swap.own_task == None:
                self.popup.hide()
                self.sp.add_component(Label("ההחלפה לא בוצעה - לא בחרת תורנות להחלפה", fg_color='red'), 0)
                return
            target_task.assignment.remove(swap.target)
            target_task.assignment.append(owner)
            swap.own_task.assignment.remove(owner)
            swap.own_task.assignment.append(swap.target)
            swap.own_task.save()
            target_task.save()
        try:
            simple_send_message(f"תורנות {target_task.start_time} - {target_task.start_time} הוחלפה", [owner, swap.target])
        except:
            print("Couldn't send message to ",  [owner.name, swap.target.name])
        self.popup.hide()
        self.select_week(curr_week_id, owner)

    def execute_self_swap(self, swap, curr_week_id, owner, own_task):
        own_task.assignment.remove(owner)
        own_task.assignment.append(swap.target)
        own_task.save()
        self.popup.hide()
        self.select_week(curr_week_id, owner)

    def open_swap_form(self, curr_week_id, user, task):
        print("target_task: " + str(task))
        form = JsonSchemaForm(CleaningSwap, visible=['target', 'one_sided', 'own_task'],
                              display_name={
                                  'target': 'את מי להחליף',
                                  'one_sided': 'חד צדדי',
                                  'own_task': 'תורנות שלי',
                              }, placeholder={
                'target': 'חניך מתלם 1',
            }, options={
                'target': task.assignment,
                'own_task': CleaningTask.objects(assignment__contains=user)
            }, options_display={
                'target': lambda x: "%d - %s" % (x.mahzor, str(x)),
                'own_task': lambda x: get_hebrew_time(x.start_time)
            }, submit=lambda x: self.execute_swap(x, curr_week_id, task, user))

        self.popup = PopUp(form, title="החלפת תורנות", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def open_self_swap_form(self, curr_week_id, user, task):
        form = JsonSchemaForm(SelfCleaningSwap, visible=['target'],
                              display_name={
                                  'target': 'מי מחליף אותך',
                              }, placeholder={
                'target': 'חניך מתלם 1',
            }, options={
                'target': list(User.objects),
            }, options_display={
                'target': lambda x: "%d - %s" % (x.mahzor, str(x)),
            }, submit=lambda x: self.execute_self_swap(x, curr_week_id, user, task))

        self.popup = PopUp(form, title="החלפת תורנות", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def save_task(self, task, obj):

        objs_to_delete = []
        for o in objs_to_delete:
            o.delete()

        task.assignment = obj.assigment

        # task.save()
        task.update_calendar_invite()
        task.save()

        self.popup.hide()

        self.select_week(self.last_selected_week, self.user)

    def edit_task(self, task):
        e = ViewCleaningTasks.EditTask(assigment=task.assignment)

        form = JsonSchemaForm(ViewCleaningTasks.EditTask, value=e, visible=['assigment'], display_name={
            'assigment': 'תורנים',
        }, placeholder={
            'assigment': 'חניך מתלם 1'
        }, options={
            'assigment': User.objects(mahzor__in=get_mahzor_number_list())
        }, options_display={
            'assigment': lambda x: "%d - %s" % (x.mahzor, str(x))
        }, submit=lambda x, t=task: self.save_task(t, x))

        # self.sp.add_component(form)

        self.popup = PopUp(form, title="עריכת תורנות", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def select_week(self, week_id, user):
        week = CleaningWeek.objects(id=week_id)[0]

        if week.a_mishmahat == user:
            self.is_edit_possible = True
            self.is_edit = True

        self.title.update_text("תורנויות " + week.name)

        self.last_selected_week = week_id

        table = GridPanel(20, 5, bg_color=COLOR_PRIMARY)
        self.container_table.add_component(table, 2, 0)

        self.container_table.delete_component(self.headers)
        self.headers = GridPanel(1, 5, bg_color=COLOR_PRIMARY_DARK)
        self.container_table.add_component(self.headers, 0, 0)
        for day_number, day in enumerate(week.days):
            day_header = StackPanel([])
            self.headers.add_component(day_header, 0, day_number)
            day_header.add_component(
                Label(translate_day_name(day.date.strftime("%A")), bold=True, size=SIZE_LARGE, fg_color='White'))
            day_header.add_component(Label(day.date.strftime("%d.%m.%y"), size=SIZE_MEDIUM, fg_color='White'))

        max_tasks_per_day = 9
        for day_number, day in enumerate(week.days):
            for i, task in enumerate(day.cleaning_duties):
                stack = StackPanel([], orientation=VERTICAL)
                table.add_component(stack, i, day_number, 1, 1)
                cell_header = StackPanel([], orientation=HORIZONTAL)
                stack.add_component(cell_header)

                if not isinstance(task, CleaningTask):
                    continue

                title_str = "%s עד %s" % (task.start_time.strftime("%H:%M"), task.end_time.strftime("%H:%M"))
                title = Label(title_str, fg_color='White', size=SIZE_MEDIUM)
                cell_header.add_component(title)

                if len(task.assignment) == 0:
                    continue

                for cadet in task.assignment:
                    try:
                        color = get_mahzor_color(cadet.mahzor) if user != cadet else '#000000'
                        guards_lbl = Label(cadet.name, bg_color=color,
                                           fg_color='#000000' if user != cadet else '#ffffff', size=SIZE_MEDIUM,
                                           width='6vw' if self.is_screenshot_mode else '10vw')
                        stack.add_component(guards_lbl)
                    except AttributeError:
                        print("ERROR: Got an assignee who is not a user")

                if cadet.mahzor == user.mahzor:
                    stack.add_component(
                        Button("החלף", lambda task=task, user=user: self.open_swap_form(week_id, user, task)))
                if self.is_edit:
                    stack.add_component(Button("ערוך", lambda t=task: self.edit_task(t), size=SIZE_MEDIUM))
                
            for i in range(max_tasks_per_day + 1 - len(day.cleaning_duties)):
                table.add_component(Label(), i + len(day.cleaning_duties), day_number)

        sunday = datetime.strptime(week.first_date, "%Y-%m-%d")

        print(sunday)

    def toggle_edit(self):
        self.is_edit = not self.is_edit
        self.select_week(self.last_selected_week, None)

    def get_page_ui(self, user):
        self.is_edit = False

        if permissions.is_user_cleaning_task_admin(user):
            self.is_edit_possible = True
            self.is_edit = True

        self.user = user

        self.sp = StackPanel([])

        self.title = Label("תורנויות שבועיות", size=SIZE_EXTRA_LARGE)
        self.sp.add_component(self.title)

        a_mishmahat_sp = StackPanel([], orientation=HORIZONTAL)
        a_mishmahat_sp.add_component(Label("א' משמעת:"))
        self.a_mishmahat = Label("עוד לא נבחר")
        a_mishmahat_sp.add_component(self.a_mishmahat)
        self.sp.add_component(a_mishmahat_sp)

        week_selected = StackPanel([], orientation=HORIZONTAL)
        self.sp.add_component(week_selected)
        week_selected.add_component(Label("בחר שבוע:", size=SIZE_LARGE))
        week_selected.add_component(
            ComboBox(get_weeks_dict(), on_changed=lambda selected_week: self.select_week(selected_week, user)))

        self.container_table = GridPanel(4, 1)
        self.sp.add_component(self.container_table)

        self.headers = GridPanel(1, 5, bg_color=COLOR_PRIMARY_DARK)
        self.container_table.add_component(self.headers, 0, 0)

        week = get_current_cleaning_week()
        if week is None:
            self.sp.add_component(Label("לא שובצו תורנויות לשבוע הקרוב עדיין"))
            return self.sp

        if week.a_mishmahat != None:
            self.a_mishmahat.update_text(text=week.a_mishmahat.name)
            if user == week.a_mishmahat:
                self.is_edit = True

        for day_number, day in enumerate(week.days):
            day_header = StackPanel([])
            self.headers.add_component(day_header, 0, day_number)
            day_header.add_component(
                Label(translate_day_name(day.date.strftime("%A")), bold=True, size=SIZE_LARGE, fg_color='White'))
            day_header.add_component(Label(day.date.strftime("%D"), size=SIZE_MEDIUM, fg_color='White'))

        self.container_table.add_component(Label("אירועים נוספים", size=SIZE_EXTRA_LARGE), 2, 0)

        buttons_panel = StackPanel([], HORIZONTAL)
        if self.is_edit_possible:
            buttons_panel.add_component(Button("מצב עריכה", lambda: self.toggle_edit()))
        self.sp.add_component(buttons_panel)

        print(week.id)
        self.select_week(week.id, user)

        return self.sp
