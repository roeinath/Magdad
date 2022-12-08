import datetime

from mongoengine import Document, StringField, DateField, ReferenceField, ListField

import web_features.logistic_events.permissions as permissions
from APIs.TalpiotAPIs.mahzors_utils import get_mahzor_year_3
from APIs.ExternalAPIs import FileToUpload, GoogleDrive
from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.LogisticEvents.logistic_event import LogisticEvent
from APIs.TalpiotAPIs.LogisticEvents.logistic_event_missions import LogisticEventMission
from APIs.TalpiotAPIs.LogisticEvents.logistic_event_status import LogisticEventStatus, LogisticEventStatusOptions
from web_framework.server_side.infastructure.components.confirmation_button import ConfirmationButton
from web_framework.server_side.infastructure.components.display_files import DisplayFile
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanelColumn
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page

DATE_FORMAT = '%d/%m/%Y'
LOGISTIC_EVENTS_DRIVE_ID = "1O6op3fUww1A7S2CkaM0-LKWVfKvytiXU"


class ViewLogisticEvents(Page):
    @staticmethod
    def get_title() -> str:
        return "אירועים לוגיסטיים"

    def __init__(self, params):
        super().__init__()
        self.sp = StackPanel([])

        self.container_table = None
        self.popup = None
        self.user = None
        self.events_stack = StackPanel([])
        self.closed_events_stack = StackPanel([])

        self.google_drive = GoogleDrive.get_instance()

    def is_user_logistic_permitted(self, logistic_object):
        return permissions.is_user_permitted(self.user) or logistic_object.is_user_permitted(self.user)

    def get_page_ui(self, user):
        self.user = user

        self.sp.add_component(Label("אירועים לוגיסטיים", size=SIZE_EXTRA_LARGE))
        self.sp.add_component(Button("יצירת אירוע חדש", self.create_new_event))

        self.sp.add_component(Label())
        self.sp.add_component(self.events_stack)
        self.sp.add_component(Label())
        self.sp.add_component(self.closed_events_stack)

        self.draw_tables()

        return self.sp

    ##########
    # TABLES #
    ##########
    def draw_tables(self):
        self.events_stack.clear()
        self.events_stack.add_component(Label(f"אירועים פתוחים", size=SIZE_LARGE))
        self.events_stack.add_component(Divider())
        self.events_stack.add_component(self.get_events_accordion(is_closed=False))

        self.closed_events_stack.clear()
        self.closed_events_stack.add_component(Label(f"אירועים סגורים", size=SIZE_LARGE))
        self.closed_events_stack.add_component(Divider())
        self.closed_events_stack.add_component(self.get_events_accordion(is_closed=True))

    def get_events_accordion(self, is_closed):
        events = LogisticEvent.objects(closed=is_closed).select_related(2)
        events = list(filter(lambda event: self.is_user_logistic_permitted(event) or is_closed,
                             events))

        event_names = [e.event_name for e in events]
        components = [self.get_event_table(event) for event in events]
        if not event_names:
            return Label("אין אירועים", size=SIZE_MEDIUM)
        events_accordion = Accordion(components, event_names)
        return events_accordion

    def get_event_table(self, event):
        sp = StackPanel([
            self.event_info_component(event),
            Divider(),
            Label("סטטוס", size=SIZE_LARGE), self.get_status_table(event),
            Divider(),
            Label("משימות", size=SIZE_LARGE), self.get_missions_table(event), self.get_missions_buttons(event),
            Divider(),
            self.action_buttons_component(event)
        ])
        return sp

    def get_status_table_colors(self, logistic_event_statuses):
        row_colors = {}
        current_status_colored = False
        for i, status in enumerate(logistic_event_statuses, start=1):
            if not status.approved and not current_status_colored:
                row_colors[i] = COLOR_LIGHT_BLUE, COLOR_BLACK
                current_status_colored = True
            if not status.relevant:
                row_colors[i] = COLOR_GRAY, COLOR_BLACK
        return row_colors

    def get_status_table(self, logistic_event: LogisticEvent):
        column_list = [
            DocumentGridPanelColumn('approved', " ", component_parser=self.approve_status_component),
            DocumentGridPanelColumn('status_name', "שם"),
            DocumentGridPanelColumn('permitted_users', "מי מאשר/ת"),
            DocumentGridPanelColumn('deadline', "דדליין", component_parser=self.deadline_component),
            DocumentGridPanelColumn('attached_file_link', "מסמך מצורף",
                                    component_parser=self.attached_file_component),
            DocumentGridPanelColumn('comments', "הערות", component_parser=self.status_comments_component),
        ]
        if self.is_user_logistic_permitted(logistic_event):
            column_list.append(
                DocumentGridPanelColumn('approved', ' ', component_parser=self.delete_object_component)
            )
        filter_by = {'event_name': logistic_event.event_name}
        order_by = ['deadline']
        logistic_event_statuses = LogisticEventStatus.objects(**filter_by).order_by(*order_by)
        row_colors = self.get_status_table_colors(logistic_event_statuses)
        table = DocumentGridPanel(LogisticEventStatus, column_list=column_list,
                                  filter_by=filter_by, order_by=order_by, row_colors=row_colors)
        return table

    def get_missions_table(self, logistic_event: LogisticEvent):
        column_list = [
            DocumentGridPanelColumn('approved', " ", component_parser=self.approve_status_component),
            DocumentGridPanelColumn('description', "משימה"),
            DocumentGridPanelColumn('users_in_charge', "מי מבצע/ת", component_parser=lambda status, users:
            self.users_list_names(status, field='users_in_charge')),
            DocumentGridPanelColumn('deadline', "דדליין", component_parser=self.deadline_component),
            DocumentGridPanelColumn('comments', "הערות", component_parser=self.status_comments_component),
        ]
        if self.is_user_logistic_permitted(logistic_event):
            column_list.append(
                DocumentGridPanelColumn('logistic_event', ' ', component_parser=self.delete_object_component)
            )
        table = DocumentGridPanel(
            LogisticEventMission, column_list=column_list,
            filter_by={'logistic_event': logistic_event}, order_by=['approved', 'deadline'],
        )
        table.update_color()
        return table

    def get_missions_buttons(self, logistic_event: LogisticEvent):
        buttons = StackPanel([])
        if self.is_user_logistic_permitted(logistic_event):
            buttons.add_component(Button("הוספת משימה ➕", lambda event=logistic_event: self.add_mission_form(event)))
        return buttons

    def delete_object_component(self, obj, *args):
        if self.is_user_logistic_permitted(obj):
            return ConfirmationButton("מחיקה", lambda o=obj: self.delete_object_and_refresh(o), bg_color="red")
        return Label("")

    def event_info_component(self, event: LogisticEvent):
        infos = [
            [Label("שם האירוע", bold=True), Label(event.event_name)],
            [Label("תאריך האירוע", bold=True), Label(event.event_date)],
            [Label("צוערים אחראיים", bold=True), self.users_list_names(event, field='cadets_in_charge')],
            [Label("סג\"ז אחראיים", bold=True), self.users_list_names(event, field='sagaz_in_charge')],
            [Label("סג\"ב אחראיים", bold=True), self.users_list_names(event, field='sagab_in_charge')],
            # [Label("סטטוס נוכחי", bold=True), self.current_status_component(event)],
        ]
        info_grid_panel = GridPanel(1, len(infos), bordered=False)
        for i, info in enumerate(infos):
            info_grid_panel.add_component(StackPanel(info), column=i)
        return info_grid_panel

    ###########
    # ACTIONS #
    ###########
    def action_buttons_component(self, logistic_event: LogisticEvent):
        button_sp = StackPanel([], orientation=HORIZONTAL)
        if permissions.is_user_permitted(self.user):
            button_sp.add_component(
                ConfirmationButton("פתיחה מחדש" if logistic_event.closed else "סגירת אירוע", bg_color="green",
                                   action=lambda event=logistic_event: self.switch_logistic_event(event))
            )
        if permissions.is_user_permitted(self.user):
            button_sp.add_component(
                ConfirmationButton("מחיקת אירוע", action=lambda event=logistic_event: self.delete_object_and_refresh(event),
                                   bg_color='red')
            )
        return button_sp

    def switch_logistic_event(self, logistic_event: LogisticEvent):
        if logistic_event is None:
            return
        logistic_event.closed = not logistic_event.closed
        if logistic_event.closed:
            self.add_folder_to_drive(logistic_event)
        logistic_event.save()
        self.draw_tables()

    def create_new_event(self):
        class NewLogisticEventForm(LogisticEvent):
            stages = ListField(ReferenceField(LogisticEventStatusOptions))

        def save_event(new_event: NewLogisticEventForm):
            folder_id = self.create_event_folder(new_event)
            event = LogisticEvent(event_name=new_event.event_name, event_date=new_event.event_date,
                                  cadets_in_charge=new_event.cadets_in_charge,
                                  sagaz_in_charge=new_event.sagaz_in_charge,
                                  sagab_in_charge=new_event.sagab_in_charge,
                                  drive_folder_id=folder_id)
            current_status = None
            for stage in reversed(new_event.stages):
                current_status = LogisticEvent.new_status_from_option(event, stage)
            event.current_status = current_status
            event.save()
            self.popup.hide()
            self.draw_tables()

        default_value = NewLogisticEventForm(stages=LogisticEventStatusOptions.objects)
        form = JsonSchemaForm(NewLogisticEventForm,
                              visible=['event_name', 'event_date', 'sagaz_in_charge', 'sagab_in_charge', 'stages'],
                              value=default_value,
                              display_name={
                                  'event_name': 'אירוע',
                                  'event_date': 'תאריך',
                                  'sagaz_in_charge': 'סגל זוטר אחראי',
                                  'sagab_in_charge': 'סגל בכיר אחראי',
                                  'stages': 'שלבים בתכנון האירוע',
                              },
                              options={
                                  'sagaz_in_charge': User.objects(mahzor=get_mahzor_year_3().mahzor_num),
                                  'sagab_in_charge': User.objects(mahzor__lt=get_mahzor_year_3().mahzor_num),
                                  'stages': LogisticEventStatusOptions.objects.order_by('-deadline_weeks_before')
                              },
                              options_display={
                                  'sagaz_in_charge': lambda x: x.get_full_name(),
                                  'sagab_in_charge': lambda x: x.get_full_name(),
                                  'stages': lambda x: x.status_name,
                              },
                              submit=save_event)

        self.popup = PopUp(form, title="פתיחת אירוע חדש", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    ############
    # MISSIONS #
    ############
    def add_mission_form(self, logistic_event: LogisticEvent):
        def add_mission(new_mission: LogisticEventMission):
            new_mission.logistic_event = logistic_event
            new_mission.users_in_charge = logistic_event.cadets_in_charge
            new_mission.save()
            self.popup.hide()
            self.draw_tables()

        default_value = LogisticEventMission.new_mission(logistic_event, description='', comments='')
        form = JsonSchemaForm(
            LogisticEventMission,
            value=default_value,
            visible=['description', 'users_in_charge', 'deadline', 'comments'],
            display_name={'description': 'משימה', 'deadline': 'דד ליין', 'comments': 'הערות',
                          'users_in_charge': 'אחראיים'},
            paragraphTexts=['comments'],
            submit=add_mission
        )

        self.popup = PopUp(form, title="הוספת משימה", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    ############
    # DEADLINE #
    ############
    def edit_status_deadline(self, status):
        def save_status(x):
            status.deadline = x.new_deadline
            status.save()
            self.draw_tables()

        class DeadlineEditForm(Document):
            new_deadline: datetime.datetime = DateField()

        form = JsonSchemaForm(
            DeadlineEditForm,
            value=DeadlineEditForm(new_deadline=status.deadline),
            visible=['new_deadline'],
            display_name={'new_deadline': 'דדליין לסיום'},
            placeholder={},
            options={},
            options_display={},
            submit=save_status
        )

        self.popup = PopUp(form, title="עריכת דדליין", is_shown=True, is_cancelable=True)
        self.events_stack.add_component(self.popup)

    def deadline_component(self, status, deadline: datetime.datetime):
        text = deadline.strftime(DATE_FORMAT) if deadline is not None else "לא הוזן"
        color = COLOR_BLACK
        if deadline < datetime.date.today():
            color = COLOR_RED if not status.approved else COLOR_GREEN
        sp = StackPanel([])
        if text:
            sp.add_component(Label(text, fg_color=color))

        if permissions.is_user_permitted(self.user):
            sp.add_component(Button("עריכה", action=lambda s=status: self.edit_status_deadline(s)))
        return sp

    ##############
    # LIST USERS #
    ##############
    def edit_object_users_in_charge(self, obj, field: str):
        def save_object(x):
            setattr(obj, field, x.users)
            obj.save()
            self.draw_tables()

        class UsersEditForm(Document):
            users: list = ListField(ReferenceField(User))

        form = JsonSchemaForm(
            UsersEditForm,
            value=UsersEditForm(users=getattr(obj, field, [])),
            visible=['users'],
            display_name={'users': 'אחראיים'},
            options={'users': User.objects},
            options_display={'users': lambda x: x.get_full_name()},
            submit=save_object
        )

        self.popup = PopUp(form, title="עריכה", is_shown=True, is_cancelable=True)
        self.events_stack.add_component(self.popup)

    def users_list_names(self, obj, field):
        names = [c.name for c in getattr(obj, field, [])]
        user_sp = StackPanel([])
        user_sp.add_component(Label(', '.join(names) if names else '---'))
        if self.is_user_logistic_permitted(obj):
            btn_action = lambda o=obj, f=field: self.edit_object_users_in_charge(o, f)
            user_sp.add_component(Button('עריכה', action=btn_action))
        return user_sp

    #########
    # FILES #
    #########
    def edit_status_attachment(self, obj):
        class AttachmentEditForm(Document):
            attached_file_link: str = StringField()

        def save_attached_file_link(x):
            obj.attached_file_link = x.attached_file_link
            obj.save()
            self.draw_tables()
            self.popup.hide()

        default_value = AttachmentEditForm(attached_file_link=obj.attached_file_link)
        form = JsonSchemaForm(AttachmentEditForm, value=default_value, visible=['attached_file_link'],
                              display_name={'attached_file_link': 'קישור לקובץ'}, submit=save_attached_file_link)
        self.popup = PopUp(form, title="עריכת קובץ מצורף", is_shown=True, is_cancelable=True)
        self.events_stack.add_component(self.popup)

        # def save_attached_file_id(files):
        #     self.popup.get_first_level_children().pop()
        #     if not files:
        #         self.popup.add_component(Label("לא הועלה קובץ", fg_color=COLOR_RED))
        #         return
        #     obj.attached_file_id = files[0].id
        #     obj.save()
        #     self.popup.add_component(Label("הקובץ הועלה בהצלחה", fg_color=COLOR_GREEN))
        #
        # upload_file = UploadFiles(save_attached_file_id)
        # self.popup = PopUp(upload_file, title="עריכת קובץ מצורף", is_shown=True, is_cancelable=True)
        # self.events_stack.add_component(self.popup)

    def attached_file_component(self, obj, attachment):
        sp = StackPanel([])
        file_display = DisplayFile(FileToUpload(name='קובץ מצורף', url=attachment, file_type='pdf'))
        sp.add_component(file_display if attachment else Label('---'))
        logistic_event = self.get_event_from_object(obj)

        if obj.is_user_permitted(self.user) or self.is_user_logistic_permitted(logistic_event):
            sp.add_component(Button("עריכה", action=lambda s=obj: self.edit_status_attachment(s)))
        return sp

    def get_event_from_object(self, obj) -> LogisticEvent:
        if isinstance(obj, LogisticEventMission):
            return obj.logistic_event
        elif isinstance(obj, LogisticEventStatus):
            return LogisticEvent.objects.get(event_name=obj.event_name)
        else:
            raise Exception("WTF")

    ############
    # COMMENTS #
    ############
    def edit_status_comments(self, obj):
        class CommentsEditForm(Document):
            comments: str = StringField()

        def save_comments(x):
            obj.comments = x.comments
            obj.save()
            self.draw_tables()
            self.popup.hide()

        default_value = CommentsEditForm(comments=obj.comments)
        form = JsonSchemaForm( CommentsEditForm, value=default_value, visible=['comments'], display_name={'comments': 'הערות'},
                               paragraphTexts=['comments'], submit=save_comments)
        self.popup = PopUp(form, title="עריכת הערות", is_shown=True, is_cancelable=True)
        self.events_stack.add_component(self.popup)

    def status_comments_component(self, obj, comments):
        sp = StackPanel([])
        sp.add_component(Label(comments if comments else '---'))
        logistic_event = self.get_event_from_object(obj)
        if obj.is_user_permitted(self.user) or self.is_user_logistic_permitted(logistic_event):
            sp.add_component(Button("עריכה", action=lambda s=obj: self.edit_status_comments(s)))
        return sp

    ###########
    # CURRENT #
    ###########
    def edit_current_status(self, event: LogisticEvent):
        def save_status(x):
            event.current_status = x.current_status
            event.save()
            self.draw_tables()
            self.popup.hide()

        form = JsonSchemaForm(
            LogisticEvent,
            value=event,
            visible=['current_status'],
            display_name={'current_status': 'סטטוס נוכחי'},
            options={'current_status': LogisticEventStatus.objects(event_name=event.event_name)},
            options_display={'current_status': lambda x: x.status_name},
            submit=save_status
        )

        self.popup = PopUp(form, title="עריכת סטטוס נוכחי", is_shown=True, is_cancelable=True)
        self.events_stack.add_component(self.popup)

    def current_status_component(self, logistic_event: LogisticEvent):
        current_status_label = Label(logistic_event.get_current_status().status_name)
        sp = StackPanel([current_status_label])
        if self.is_user_logistic_permitted(logistic_event):
            sp.add_component(Button("עריכה", action=lambda e=logistic_event: self.edit_current_status(e)))
        return sp

    def delete_object_and_refresh(self, obj):
        if obj is None:
            return
        obj.delete()
        self.draw_tables()

    ###########
    # APPROVE #
    ###########

    def approve_status_component(self, obj, *args):
        colors = {True: 'green', False: 'red', None: 'orange'}
        button_labels = {True: '✔️', False: '❌', None: '⌛'}
        boolean_cycle = {True: False, False: None, None: True}

        def update_status():
            if self.is_user_logistic_permitted(obj):
                obj.approved = boolean_cycle[obj.approved]
                obj.save()
                approve_button.update_text(text=button_labels[obj.approved])
                approve_button.update_color(bg_color=colors[obj.approved])

        approve_button = Button(button_labels[obj.approved], action=update_status, bg_color=colors[obj.approved])
        message = "שינוי סטטוס ע\"י לחיצה"
        if hasattr(obj, 'relevant') and not obj.relevant:
            approve_button = Button('✖️', bg_color=COLOR_GRAY)
            message = "לא רלוונטי"
        return StackPanel([approve_button, Label(message, size=SIZE_SMALL)])

    #########
    # DRIVE #
    #########

    def create_event_folder(self, event: LogisticEvent):
        if event.drive_folder_id:
            return
        folder_name = f"{event.event_name} {event.event_date.strftime(DATE_FORMAT)}"
        folder = self.google_drive.create_folder(folder_name, LOGISTIC_EVENTS_DRIVE_ID)
        return folder['id']

    def add_folder_to_drive(self, logistic_event: LogisticEvent):
        logistic_event.drive_folder_id = self.create_event_folder(logistic_event)
        for status in LogisticEventStatus.objects(event_name=logistic_event.event_name):
            # TODO: move files of status to folder
            pass
        logistic_event.save()
