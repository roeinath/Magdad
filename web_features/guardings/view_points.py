# from general import *
from APIs.TalpiotAPIs.Tasks.task import Task
from APIs.TalpiotAPIs.Tasks.dummy_task import DummyTask
from APIs.TalpiotAPIs.Tasks.task_type import TaskType
from web_features.guardings import permissions
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.constants import *

from APIs.TalpiotAPIs import User

from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.constants import *
from APIs.TalpiotAPIs.mahzors_utils import *
from web_features.guardings.logic.calculate_guarding_points import calculate_guarding_points


class ViewPoints(Page):
    @staticmethod
    def get_title() -> str:
        return "הצגת נקודות שמירה"

    @staticmethod
    def is_authorized(user):
        return MATLAM in user.role  # Only the people of the base

    def __init__(self, params):
        super().__init__()
        self.sp = None

    def show_user_tasks(self):
        pass

    def add_dummy_task(self, task):
        task.save()

    def open_add_dummy_task(self):
        form = JsonSchemaForm(DummyTask, visible=['users', 'points', 'description', 'date'], display_name={
            'users': 'משתתפים',
            'points': 'נקודות',
            'description': 'תיאור',
            'date': 'תאריך'
        }, placeholder={
            'users': '[]',
            'points': '0',
            'description': '...סיבה',
            'date': '0000-00-00'
        }, options={
            'users': User.objects,
        }, options_display={
            'users': lambda x: "%d - %s" % (x.mahzor, str(x))
        },
                              submit=lambda x: self.add_dummy_task(x))

        self.popup = PopUp(form, title="יצירת שמירת דמה", is_shown=True, is_cancelable=False)
        self.sp.add_component(self.popup)

    def draw_table(self, mahzor, user=None):
        mahzor = int(mahzor)

        all_users = list(User.objects(mahzor=mahzor))
        table = GridPanel(len(all_users), 2, bg_color=COLOR_PRIMARY_DARK)

        users_points = calculate_guarding_points(all_users)

        all_users.sort(key=lambda x: users_points[x], reverse=True)
        print("done calculation")

        for i,u in enumerate(all_users):
            if u not in users_points:
                users_points[u] = 0
            points = users_points[u]
            color = COLOR_TRANSPARENT
            if u.name == user.name:
                color = COLOR_PRIMARY_LIGHT
            table.add_component(Label(str(u.name), fg_color='White'), i, 0, bg_color=color)
            table.add_component(Label(str(points), fg_color='White'), i, 1, bg_color=color)
        
        self.layout_table.add_component(table, 1, 0)

    def get_page_ui(self, user):
        self.sp = StackPanel([])

        self.sp.add_component(Label("נקודות שמירה", size=SIZE_EXTRA_LARGE))

        if permissions.is_user_guarding_admin(user):
            self.sp.add_component(Button("הוסף אירוע מדומה", self.open_add_dummy_task))

        mahzor_options = {m.mahzor_num: m.short_name for m in get_mahzors()}
        self.sp.add_component(ComboBox(mahzor_options, lambda s: self.draw_table(s, user),
                                       default_value=str(user.mahzor)))

        self.layout_table = GridPanel(2, 1)

        headers = GridPanel(1, 2, bg_color=COLOR_PRIMARY_DARK)
        headers.add_component(Label("צוער/ת", fg_color='White', size=SIZE_LARGE), 0, 0)
        headers.add_component(Label("נקודות", fg_color='White', size=SIZE_LARGE), 0, 1)
        self.layout_table.add_component(headers, 0, 0)

        self.sp.add_component(self.layout_table)
        self.draw_table(str(user.mahzor), user)

        return self.sp
