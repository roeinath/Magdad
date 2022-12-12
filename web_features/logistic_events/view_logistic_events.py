from mongoengine import ReferenceField, ListField, Q

import web_features.logistic_events.permissions as permissions
from APIs.TalpiotAPIs.LogisticEvents.logistic_event import LogisticEvent
from APIs.TalpiotAPIs.LogisticEvents.logistic_event_status import LogisticEventStatusOptions, LogisticEventStatus
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.mahzors_utils import get_mahzor_year_3
from web_features.logistic_events.logistic_comonnents import *
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.confirmation_button import ConfirmationButton
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page


class ViewLogisticEvents(Page):
    @staticmethod
    def get_title() -> str:
        return "מעקב אירועים"

    def __init__(self, params):
        super().__init__()
        self.sp = StackPanel([])

        self.popup = None
        self.user = None
        self.events_stack = StackPanel([])
        self.closed_events_stack = StackPanel([])

        self.external_google_manager = LogisticExternalGoogleManager()
        self.general_logistic_components = GeneralLogisticComponents(self, self.external_google_manager)
        self.status_table = LogisticStatusTable(self, self.external_google_manager)
        self.mission_table = LogisticMissionTable(self, self.external_google_manager)

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
        if permissions.is_user_permitted(self.user) or is_closed:
            events = LogisticEvent.objects.filter(closed=is_closed).select_related(1)
        else:
            query = Q(closed=is_closed) & \
                    (Q(cadets_in_charge=self.user) | Q(sagaz_in_charge=self.user) | Q(sagab_in_charge=self.user))
            events = LogisticEvent.objects.filter(query).select_related(1)

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
            Label("סטטוס", size=SIZE_LARGE), self.status_table.get_status_table(event),
            Divider(),
            Label("משימות", size=SIZE_LARGE), self.mission_table.get_missions_table(event),
            self.mission_table.get_missions_buttons(event),
            Divider(),
            self.action_buttons_component(event)
        ])
        return sp

    def event_info_component(self, event: LogisticEvent):
        infos = [
            [Label("שם האירוע", bold=True), Label(event.event_name)],
            [Label("תאריך האירוע", bold=True), Label(event.event_date)],
            [Label("צוערים אחראיים", bold=True), self.general_logistic_components.users_list_names(
                event, field='cadets_in_charge')],
            [Label("סג\"ז אחראיים", bold=True), self.general_logistic_components.users_list_names(
                event, field='sagaz_in_charge')],
            [Label("סג\"ב אחראיים", bold=True), self.general_logistic_components.users_list_names(
                event, field='sagab_in_charge')],
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
            delete_button = ConfirmationButton(
                "מחיקת אירוע",
                action=lambda: self.general_logistic_components.delete_object_and_refresh(logistic_event),
                bg_color=COLOR_RED
            )
            button_sp.add_component(delete_button)
        return button_sp

    def switch_logistic_event(self, logistic_event: LogisticEvent):
        if logistic_event is None:
            return
        logistic_event.closed = not logistic_event.closed
        if logistic_event.closed:
            self.external_google_manager.add_folder_to_drive(logistic_event)
        logistic_event.save()
        self.draw_tables()

    def create_new_event(self):
        class NewLogisticEventForm(LogisticEvent):
            stages = ListField(ReferenceField(LogisticEventStatusOptions))

        def save_event(new_event: NewLogisticEventForm):
            folder_id = self.external_google_manager.create_event_folder(new_event)
            event = LogisticEvent(event_name=new_event.event_name, event_date=new_event.event_date,
                                  cadets_in_charge=new_event.cadets_in_charge,
                                  sagaz_in_charge=new_event.sagaz_in_charge,
                                  sagab_in_charge=new_event.sagab_in_charge,
                                  drive_folder_id=folder_id)
            for stage in new_event.stages:
                current_status = LogisticEvent.new_status_from_option(event, stage)
                print(current_status.status_name, current_status.event_name)
                self.external_google_manager.insert_event_to_calendar(event, current_status)
                event.statuses.append(current_status)

            event.current_status = event.statuses[0]
            event.save()
            self.popup.hide()
            self.draw_tables()

        status_options = LogisticEventStatusOptions.objects().order_by('-deadline_weeks_before')
        status_options = sorted(status_options, key=lambda x: -x.deadline_weeks_before)

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
                                  'stages': status_options
                              },
                              options_display={
                                  'sagaz_in_charge': lambda x: x.get_full_name(),
                                  'sagab_in_charge': lambda x: x.get_full_name(),
                                  'stages': lambda x: x.status_name,
                              },
                              submit=save_event)

        self.popup = PopUp(form, title="פתיחת אירוע חדש", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def delete_event(self, event: LogisticEvent):
        if event is None:
            return
        event.delete()
        for status in LogisticEventStatus.objects(event_name=event.event_name):
            status.delete()
        self.draw_tables()
