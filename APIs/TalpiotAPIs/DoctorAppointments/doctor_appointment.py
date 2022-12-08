import datetime

from mongoengine import Document, ReferenceField, DateTimeField

from APIs.TalpiotAPIs.User.user import User


class DoctorAppointment(Document):
    meta = {'collection': 'doctor_appointments'}

    time: datetime.datetime = DateTimeField()
    patient: User = ReferenceField(User)

    def to_string(self):
        s = "תאריך:"
        s += str(self.time.day)
        s += "." + str(self.time.month)
        s += " בשעה "
        s += self.time.strftime("%H:%M:%S")
        return s
