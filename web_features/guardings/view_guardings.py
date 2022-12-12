# from general import *

# import cloudinary
# import cloudinary.uploader
from APIs.TalpiotAPIs.Tasks.dummy_task import DummyTask
from APIs.TalpiotAPIs.Tasks.guarding.guarding_week import GuardingWeek
from APIs.TalpiotAPIs.Tasks.task import Task
from APIs.TalpiotAPIs.static_fields import get_mahzor_number_list
from web_features.guardings import permissions
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.actions import simple_send_message
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.constants import *
# from web_features.guardings.logic.export_guardings.export_guardings import ExportGuardingWeek

import datetime

from APIs.TalpiotAPIs import User
from mongoengine import *

from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel, VERTICAL, HORIZONTAL
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.page import Page

from APIs.TalpiotAPIs.mahzors_utils import *


DAY_LABEL_FORMAT = 'עלמ"ש ביום {day_name}'
GUARDING_TIME_FORMAT = 'יום {day_name} מ-{start_time} עד {end_time}'


def get_current_guarding_week():
    x = GuardingWeek.objects(first_date=str(get_current_sunday()))
    if x:
        return x[0]
    weeks = GuardingWeek.objects()
    return weeks[len(weeks) - 1]


def get_weeks_dict():
    res = {}
    for week in GuardingWeek.objects():
        res[str(week.id)] = week.name
    return res


class GuardingSwap(Document):
    target: User = ReferenceField(User)
    one_sided: bool = BooleanField()
    own_task = ReferenceField(Task)


class SelfGuardingSwap(Document):
    target: User = ListField(ReferenceField(User))


class ViewGuardings(Page):
    @staticmethod
    def get_title() -> str:
        return "הצגת שמירות"

    def __init__(self, params):
        super().__init__()
        self.headers = None
        self.container_table = None
        self.popup = None

        self.is_edit = False
        self.last_selected_week = None
        self.additional_table = None

        self.current_week = None
        self.selected_kaztar_label = None

        self.user = None
        self.DIRECTORY_ID = '1vrh93tqqGSrpYhswTRG_Vdy8DDMFaaLi'

    def get_page_ui(self, user):
        self.user = user

        self.sp = StackPanel([])

        self.title = Label("שמירות שבועיות", size=SIZE_EXTRA_LARGE)
        self.sp.add_component(self.title)

        kaztar_sp = StackPanel([], orientation=HORIZONTAL)
        kaztar_sp.add_component(Label("קצתר:"))
        self.selected_kaztar_label = Label("עוד לא נבחר")
        kaztar_sp.add_component(self.selected_kaztar_label)
        self.sp.add_component(kaztar_sp)

        week_selected = StackPanel([], orientation=HORIZONTAL)
        self.sp.add_component(week_selected)
        week_selected.add_component(Label("בחר שבוע:", size=SIZE_LARGE))
        week_selected.add_component(
            ComboBox(get_weeks_dict(), on_changed=lambda selected_week: self.show_week(selected_week, user)))

        self.container_table = GridPanel(5, 1)
        self.sp.add_component(self.container_table)

        self.headers = GridPanel(1, 5, bg_color=COLOR_PRIMARY_DARK)
        self.container_table.add_component(self.headers, 0, 0)

        week = get_current_guarding_week()
        if week is None:
            self.sp.add_component(Label("לא שובצו שמירות לשבוע הקרוב עדיין"))
            return self.sp

        else:
            for day_number, day in enumerate(week.days):
                day_header = StackPanel([])
                self.headers.add_component(day_header, 0, day_number)
                day_header.add_component(
                    Label(translate_day_name(day.date.strftime("%A")), bold=True, size=SIZE_LARGE, fg_color='White'))
                day_header.add_component(Label(day.date.strftime("%D"), size=SIZE_MEDIUM, fg_color='White'))

            self.container_table.add_component(Label("אירועים נוספים", size=SIZE_EXTRA_LARGE), 3, 0)

            self.show_week(week.id, user)

            return self.sp

    def show_week(self, week_id, user):
        week = GuardingWeek.objects.get(id=week_id)
        self.current_week = week

        self.title.update_text("שמירות " + week.name)

        self.last_selected_week = week_id

        self.is_edit = False
        if week.kaztar is not None:
            self.selected_kaztar_label.update_text(text=week.kaztar.name)
            if user == week.kaztar:
                self.is_edit = True

        if permissions.is_user_guarding_admin(user):
            self.is_edit = True

        table = GridPanel(20, 5, bg_color=COLOR_PRIMARY)
        self.container_table.add_component(table, 2, 0)

        self.container_table.delete_component(self.headers)
        self.headers = GridPanel(1, 5, bg_color=COLOR_PRIMARY_DARK)
        self.container_table.add_component(self.headers, 0, 0)
        for day_number, day in enumerate(week.days):
            day_header = StackPanel([])
            self.headers.add_component(day_header, 0, day_number)
            day_header.add_component(
                Label(DAY_LABEL_FORMAT.format(day_name=translate_day_name(day.date.strftime("%A"))),
                      bold=True, size=SIZE_LARGE, fg_color='White'))
            day_header.add_component(Label(day.date.strftime("%d.%m.%y"), size=SIZE_MEDIUM, fg_color='White'))
        for day_number, day in enumerate(week.days):
            for i, task in enumerate(day.guardings):
                stack = StackPanel([], orientation=VERTICAL)
                table.add_component(stack, i, day_number, 1, 1)
                cell_header = StackPanel([], orientation=HORIZONTAL)
                stack.add_component(cell_header)

                title_str = GUARDING_TIME_FORMAT.format(day_name=translate_day_name(task.start_time.strftime("%A")),
                                                        start_time=task.start_time.strftime("%H:%M"),
                                                        end_time=task.end_time.strftime("%H:%M"))
                title = Label(title_str, fg_color='White', size=SIZE_MEDIUM)
                cell_header.add_component(title)
                if task.task_type.description:
                    description_str = "(%s)" % task.task_type.description
                    description = Label(description_str, fg_color='White', size=SIZE_SMALL)
                    cell_header.add_component(description)

                for guard in task.assignment:
                    color = get_mahzor_color(guard.mahzor) if user != guard else '#000000'
                    guards_lbl = Label(guard.name, bg_color=color, fg_color='#000000' if user != guard else '#ffffff',
                                       size=SIZE_MEDIUM, width='10vw')
                    stack.add_component(guards_lbl)

                if user in task.assignment:
                    stack.add_component(Button("החלף שמירה שלי",
                                               lambda task=task, user=user: self.open_self_swap_form(week_id, user,
                                                                                                     task)))
                stack.add_component(
                    Button("החלף", lambda task=task, user=user: self.open_swap_form(week_id, user, task)))
                if self.is_edit:
                    stack.add_component(Button("ערוך", lambda t=task: self.show_edit_task_form(t), size=SIZE_MEDIUM))

        sunday = datetime.strptime(week.first_date, "%Y-%m-%d")

        dummy_task_list = list(DummyTask.objects(date__gte=sunday, date__lt=sunday + timedelta(days=7)))

        self.additional_table = GridPanel(len(dummy_task_list) + 1, 4)
        self.container_table.add_component(self.additional_table, 4, 0)

        additional_table_headers = ["אירוע", "משתתפים", "נקודות לכל משתתף", "תאריך"]

        for i, header_text in enumerate(additional_table_headers):
            self.additional_table.add_component(Label(header_text, size=SIZE_MEDIUM, fg_color="white"), 0, i,
                                                bg_color=COLOR_PRIMARY_DARK)

        for i, task in enumerate(dummy_task_list):
            self.additional_table.add_component(Label(task.description), i + 1, 0)
            self.additional_table.add_component(Label(", ".join(list(map(lambda x: str(x), task.users)))), i + 1, 1)
            self.additional_table.add_component(Label(task.points), i + 1, 2)
            self.additional_table.add_component(Label(task.date.strftime("%d/%m/%Y")), i + 1, 3)

    def save_task(self, task, obj):
        task.assignment = obj.assigment

        task.update_calendar_invite()
        task.save()

        message_text = f"התבצעה החלפת שמירה בין {task.assignment} לבין {obj.assigment} על ידי {self.user.name}"
        simple_send_message(text=message_text, user_list=obj.assigment+task.assignment)

        self.popup.hide()

        self.show_week(self.last_selected_week, self.user)

    def show_edit_task_form(self, task):

        class EditTaskForm(Document):
            assigment = ListField(ReferenceField(User))

        e = EditTaskForm(assigment=task.assignment)

        form = JsonSchemaForm(EditTaskForm, value=e, visible=['assigment'], display_name={
            'assigment': 'שומרים',
        }, placeholder={
            'assigment': 'צוער/ת מתלם 1'
        }, options={
            'assigment': User.objects(mahzor__in=get_mahzor_number_list())
        }, options_display={
            'assigment': lambda x: "%d - %s" % (x.mahzor, str(x))
        }, submit=lambda x, t=task: self.save_task(t, x))

        self.popup = PopUp(form, title="עריכת שמירה", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def execute_swap(self, swap: GuardingSwap, curr_week_id, target_task: Task, owner):
        print("=======" + str(target_task.assignment))
        if swap.one_sided:
            target_task.assignment.remove(swap.target)
            target_task.assignment.append(owner)
            target_task.update_calendar_invite()
            target_task.save()
        else:
            if swap.target is None or swap.own_task is None:
                self.popup.hide()
                self.sp.add_component(Label("ההחלפה לא בוצעה - לא בחרת שמירה להחלפה", fg_color='red'), 0)
                return
            target_task.assignment.remove(swap.target)
            target_task.assignment.append(owner)

            swap.own_task.assignment.remove(owner)
            swap.own_task.assignment.append(swap.target)

            target_task.update_calendar_invite()
            swap.own_task.update_calendar_invite()

            swap.own_task.save()
            target_task.save()

        message_text = f"התבצעה החלפת שמירה בין {swap.target} לבין {owner} על ידי {self.user.name}"
        simple_send_message(text=message_text, user_list=[swap.target, owner])

        self.popup.hide()
        self.show_week(curr_week_id, owner)

    def execute_self_swap(self, swap: SelfGuardingSwap, curr_week_id, owner, own_task: Task):
        if swap.target is None or len(swap.target) != 1:
            return
        target = swap.target[0]
        own_task.assignment.remove(owner)
        own_task.assignment.append(target)
        own_task.update_calendar_invite()
        own_task.save()

        message_text = f"התבצעה החלפת שמירה בין {target} לבין {owner} על ידי {self.user.name}"
        simple_send_message(text=message_text, user_list=[target, owner])

        self.popup.hide()
        self.show_week(curr_week_id, owner)

    def open_swap_form(self, curr_week_id, user, task):
        print("target_task: " + str(task))
        form = JsonSchemaForm(GuardingSwap, visible=['target', 'one_sided', 'own_task'],
                              display_name={
                                  'target': 'את מי להחליף',
                                  'one_sided': 'חד צדדי',
                                  'own_task': 'שמירה שלי',
                              }, placeholder={
                'target': 'חניך מתלם 1',
            }, options={
                'target': task.assignment,
                'own_task': Task.objects(assignment__contains=user)
            }, options_display={
                'target': lambda x: "%d - %s" % (x.mahzor, str(x)),
                'own_task': lambda x: get_hebrew_time(x.start_time)
            }, submit=lambda x: self.execute_swap(x, curr_week_id, task, user))

        self.popup = PopUp(form, title="החלפת שמירה", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def open_self_swap_form(self, curr_week_id, user, task):
        form = JsonSchemaForm(SelfGuardingSwap, visible=['target'],
                              display_name={
                                  'target': 'מי מחליף אותך',
                              }, placeholder={
                'target': 'חניך מתלם 1',
            }, options={
                'target': list(User.objects(mahzor__in=get_mahzor_number_list())),
            }, options_display={
                'target': lambda x: "%d - %s" % (x.mahzor, str(x)),
            }, submit=lambda x: self.execute_self_swap(x, curr_week_id, user, task))

        self.popup = PopUp(form, title="החלפת שמירה", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def toggle_screenshot_mode(self):
        if self.is_screenshot_mode:
            self.is_screenshot_mode = False
        else:
            self.is_edit = False
            self.is_screenshot_mode = True
        self.show_week(self.last_selected_week, None)

    def toggle_edit(self):
        self.is_edit = not self.is_edit
        self.show_week(self.last_selected_week, None)

    def on_kaztar_changed(self, new_kaztar_id):
        new_kaztar = User.objects(id=new_kaztar_id)[0]
        self.current_week.kaztar = new_kaztar
        self.current_week.save()

    # def export_guardings_show(self):
    #     export_guarding = ExportGuardingWeek(self.current_week, "guardings.png")
    #     image_path = export_guarding.get_guarding_photo()
    #     cloudinary.config(cloud_name="dkcfmcnds", api_key="955946116529915", api_secret="r2Jp7VeuHuC79TytvNNKT5BJPRs",
    #                       secret=True)
    #     response = cloudinary.uploader.upload(image_path)
    #     url = response['secure_url']
    #     os.remove(image_path)
    #     guarding_image = Image(url, 0.4)
    #     display_file = DisplayFile(FileToUpload("guardings", url=url))
    #     self.popup = PopUp(guarding_image, title="הצגת תמונה", is_shown=True, is_cancelable=True)
    #     self.sp.add_component(self.popup)
