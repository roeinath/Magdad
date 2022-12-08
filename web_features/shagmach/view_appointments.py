from web_features.shagmach import permissions
from web_framework.server_side.infastructure.components.stack_panel import HORIZONTAL
from web_framework.server_side.infastructure.page import Page
from APIs.TalpiotAPIs import User
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.Image import Image
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.constants import *

from APIs.TalpiotAPIs.DoctorAppointments.doctor_appointment_day import DoctorAppointmentDay
from APIs.TalpiotAPIs.DoctorAppointments.doctor_appointment import DoctorAppointment

import datetime


class ViewDoctorAppointments(Page):
    @staticmethod
    def get_title():
        return "תורי מרפאה"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_medical_allowed(user)

    def __init__(self, params):
        super().__init__()
        self.sp = None

    def get_page_ui(self, user: User):
        self.sp = StackPanel([])
        
        self.sp.add_component(Label("תורים לרופא", size=SIZE_EXTRA_LARGE))

        for day in DoctorAppointmentDay.objects(date__gte=datetime.date.today()):
            self.sp.add_component(Label(day.date, size=SIZE_LARGE))
            daily_slots_table = GridPanel(len(day.appointments) + 1, 3, bg_color=COLOR_PRIMARY)
            daily_slots_table.add_component(Label("שעה", size=SIZE_MEDIUM, fg_color="white"), 0, 0,
                                            bg_color=COLOR_PRIMARY_DARK)
            daily_slots_table.add_component(Label("שם", size=SIZE_MEDIUM, fg_color="white"), 0, 1,
                                            bg_color=COLOR_PRIMARY_DARK)

            for i, slot in enumerate(day.appointments):
                daily_slots_table.add_component(Label(slot.to_string(), size=SIZE_MEDIUM), i + 1, 0)
                patient_name = "לא משובץ" if slot.patient is None else slot.patient.name
                color_label = "gray" if slot.patient is None else "black"
                daily_slots_table.add_component(Label(patient_name, size=SIZE_MEDIUM, fg_color=color_label), i + 1, 1)

            self.sp.add_component(daily_slots_table)

        return self.sp
