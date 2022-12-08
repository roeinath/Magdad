import copy
import datetime
from datetime import timedelta
from typing import List

from mongoengine import Document, ReferenceField, ListField, DateField

from APIs.TalpiotAPIs.DoctorAppointments.doctor_appointment import DoctorAppointment


class DoctorAppointmentDay(Document):
    meta = {'collection': 'doctor_appointment_days'}

    date: datetime.date = DateField()
    appointments: List[DoctorAppointment] = ListField(ReferenceField(DoctorAppointment))


def get_new_appointment_day(date: datetime.date):
    day = DoctorAppointmentDay(date=date)
    # appointments will be between 15:00 and 19:00 and each one will take 10 minutes
    START_TIME = datetime.datetime.combine(date, datetime.time(hour=15, minute=00))
    END_TIME = datetime.datetime.combine(date, datetime.time(hour=19, minute=00))
    APPOINTMENT_MINUTES = 10

    appointments = []
    new_appointment_time = START_TIME
    time_left = (END_TIME - new_appointment_time).total_seconds() / 60
    # make sure there is enough time to the appointment and open one up
    while APPOINTMENT_MINUTES <= time_left:
        appointments.append(DoctorAppointment(time=new_appointment_time, patient=None))
        new_appointment_time = new_appointment_time + timedelta(minutes=APPOINTMENT_MINUTES)
        time_left -= APPOINTMENT_MINUTES

    for app in appointments:
        app.save()
    day.appointments = appointments
    return day
