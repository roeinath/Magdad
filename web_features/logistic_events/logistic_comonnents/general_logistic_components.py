import datetime

from mongoengine import Document, DateField, ListField, ReferenceField, StringField

from APIs.ExternalAPIs import FileToUpload
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.LogisticEvents.logistic_event import LogisticEvent
from APIs.TalpiotAPIs.LogisticEvents.logistic_event_missions import LogisticEventMission
from APIs.TalpiotAPIs.LogisticEvents.logistic_event_status import LogisticEventStatus
from web_features.logistic_events import permissions
from web_features.logistic_events.logistic_comonnents.logistic_external_google_manager import DATE_FORMAT, \
    LogisticExternalGoogleManager
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.confirmation_button import ConfirmationButton
from web_framework.server_side.infastructure.components.display_files import DisplayFile
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.constants import *


class GeneralLogisticComponents:

    def __init__(self, logistic_page, external_google_manager: LogisticExternalGoogleManager):
        self.logistic_page = logistic_page
        self.external_google_manager = external_google_manager

    def is_user_logistic_permitted(self, *args, **kwargs):
        return self.logistic_page.is_user_logistic_permitted(*args, **kwargs)

    @staticmethod
    def get_event_from_object(obj) -> LogisticEvent:
        if isinstance(obj, LogisticEventMission):
            return obj.logistic_event
        elif isinstance(obj, LogisticEventStatus):
            return LogisticEvent.objects.get(event_name=obj.event_name)
        else:
            raise Exception("WTF")

    def draw_tables(self, *args, **kwargs):
        return self.logistic_page.draw_tables(*args, **kwargs)

    ##########
    # DELETE #
    ##########

    def delete_object_component(self, obj, *args):
        if self.is_user_logistic_permitted(obj):
            return ConfirmationButton("מחיקה", lambda o=obj: self.delete_object_and_refresh(o), bg_color=COLOR_RED)
        return Label("")

    def delete_object_and_refresh(self, obj):
        if obj is None:
            return
        obj.delete()
        self.draw_tables()

    ############
    # DEADLINE #
    ############
    def edit_status_deadline(self, status):
        class DeadlineEditForm(Document):
            new_deadline: datetime.datetime = DateField()

        def save_status(deadline: DeadlineEditForm):
            status.deadline = deadline.new_deadline
            status.save()
            self.draw_tables()

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

        self.logistic_page.popup = PopUp(form, title="עריכת דדליין", is_shown=True, is_cancelable=True)
        self.logistic_page.events_stack.add_component(self.logistic_page.popup)

    def deadline_component(self, status, deadline: datetime.datetime, logistic_event: LogisticEvent = None):
        text = deadline.strftime(DATE_FORMAT) if deadline is not None else "לא הוזן"
        color = COLOR_BLACK
        if deadline < datetime.date.today():
            color = COLOR_RED if not status.approved else COLOR_GREEN
        sp = StackPanel([])
        if text:
            sp.add_component(Label(text, fg_color=color))

        if permissions.is_user_permitted(self.logistic_page.user):
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

        self.logistic_page.popup = PopUp(form, title="עריכה", is_shown=True, is_cancelable=True)
        self.logistic_page.events_stack.add_component(self.logistic_page.popup)

    def users_list_names(self, obj, field):
        names = [c.name for c in getattr(obj, field, [])]
        user_sp = StackPanel([])
        user_sp.add_component(Label(', '.join(names) if names else '---'))
        if self.is_user_logistic_permitted(obj):
            button = Button('עריכה', action=lambda o=obj, f=field: self.edit_object_users_in_charge(o, f))
            user_sp.add_component(button)
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
            self.logistic_page.popup.hide()

        default_value = AttachmentEditForm(attached_file_link=obj.attached_file_link)
        form = JsonSchemaForm(AttachmentEditForm, value=default_value, visible=['attached_file_link'],
                              display_name={'attached_file_link': 'קישור לקובץ'}, submit=save_attached_file_link)
        self.logistic_page.popup = PopUp(form, title="עריכת קובץ מצורף", is_shown=True, is_cancelable=True)
        self.logistic_page.events_stack.add_component(self.logistic_page.popup)

        # def save_attached_file_id(files):
        #     self.logistic_page.popup.get_first_level_children().pop()
        #     if not files:
        #         self.logistic_page.popup.add_component(Label("לא הועלה קובץ", fg_color=COLOR_RED))
        #         return
        #     obj.attached_file_id = files[0].id
        #     obj.save()
        #     self.logistic_page.popup.add_component(Label("הקובץ הועלה בהצלחה", fg_color=COLOR_GREEN))
        #
        # upload_file = UploadFiles(save_attached_file_id)
        # self.logistic_page.popup = PopUp(upload_file, title="עריכת קובץ מצורף", is_shown=True, is_cancelable=True)
        # self.logistic_page.events_stack.add_component(self.logistic_page.popup)

    def attached_file_component(self, obj, attachment, logistic_event: LogisticEvent = None):
        sp = StackPanel([])
        file_display = DisplayFile(FileToUpload(name='קובץ מצורף', url=attachment))
        sp.add_component(file_display if attachment else Label('---'))
        if logistic_event is None:
            logistic_event = self.get_event_from_object(obj)

        if self.is_user_logistic_permitted(logistic_event):
            sp.add_component(Button("עריכה", action=lambda s=obj: self.edit_status_attachment(s)))
        return sp

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
            self.logistic_page.popup.hide()

        default_value = CommentsEditForm(comments=obj.comments)
        form = JsonSchemaForm(CommentsEditForm, value=default_value, visible=['comments'],
                              display_name={'comments': 'הערות'}, paragraphTexts=['comments'], submit=save_comments)
        self.logistic_page.popup = PopUp(form, title="עריכת הערות", is_shown=True, is_cancelable=True)
        self.logistic_page.events_stack.add_component(self.logistic_page.popup)

    def status_comments_component(self, obj, comments, logistic_event: LogisticEvent = None):
        sp = StackPanel([])
        sp.add_component(Label(comments if comments else '---'))
        if logistic_event is None:
            logistic_event = self.get_event_from_object(obj)
        if self.is_user_logistic_permitted(logistic_event):
            sp.add_component(Button("עריכה", action=lambda s=obj: self.edit_status_comments(s)))
        return sp

    ###########
    # APPROVE #
    ###########

    def approve_status_component(self, obj, *args):
        colors = {True: COLOR_GREEN, False: COLOR_RED, None: COLOR_YELLOW}
        button_labels = {True: '✔️', False: '❌', None: '⌛'}
        boolean_cycle = {True: False, False: None, None: True}

        def update_status():
            if self.is_user_logistic_permitted(obj):
                obj.approved = boolean_cycle[obj.approved]
                obj.save()
                approve_button.update_text(text=button_labels[obj.approved])
                approve_button.update_color(bg_color=colors[obj.approved])
            else:
                self.logistic_page.popup = PopUp(Label("אין לך הרשאות לשנות סטטוס זה"), title='', is_shown=True,
                                                 is_cancelable=True)
                self.logistic_page.events_stack.add_component(self.logistic_page.popup)

        approve_button = Button(button_labels[obj.approved], action=update_status, bg_color=colors[obj.approved])
        message = "שינוי סטטוס ע\"י לחיצה"
        if hasattr(obj, 'relevant') and not obj.relevant:
            approve_button = Button('✖️', bg_color=COLOR_GRAY)
            message = "לא רלוונטי"
        return StackPanel([approve_button, Label(message, size=SIZE_SMALL)])
