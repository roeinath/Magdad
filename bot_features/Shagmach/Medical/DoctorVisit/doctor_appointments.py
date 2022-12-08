from APIs.ExternalAPIs import *
from APIs.TalpiotAPIs import *

from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.button import Button
from bot_framework.ui.ui import UI

from APIs.TalpiotAPIs.DoctorAppointments.doctor_appointment import DoctorAppointment
from APIs.TalpiotAPIs.DoctorAppointments.doctor_appointment_day import DoctorAppointmentDay, get_new_appointment_day
from APIs.TalpiotSystem.bot_scheduled_job import remove_by_rule
from bot_features.SystemFeatures.HierarchicalMenu.Code.hierarchical_menu import HierarchicalMenu


class DoctorVisit(BotFeature):

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)

    def is_admin_authorized(self, user):
        return user.name in ['גיא דניאל הדס', 'יהלי אקשטיין', 'תומר זילברמן', 'לשם כהן פלח']

    def main(self, session: Session):
        self.ui.clear(session)
        buttons = [
            Button("צפייה בתורים שלי", self.view_my_appointments),
            Button("קביעת תור חדש", self.make_appointment),
        ]
        if self.is_admin_authorized(session.user):
            buttons.extend([
                Button("יצירת יום תורים", self.make_appointment_day),
                Button("שלח תזכורת למחר", self.remind_all_appointments)
            ])
        buttons.append(Button("🔙", lambda s: self.return_to_menu(s)))
        self.ui.create_button_group_view(session, "מה ברצונך לעשות?", buttons).draw()

    def make_appointment_day(self, session: Session):
        self.ui.clear(session)
        self.ui.create_date_choose_view(session, self.new_date_selected).draw()

    def new_date_selected(self, _, session: Session, date: datetime.date):
        self.ui.clear(session)
        if date < datetime.date.today():
            self.ui.create_date_choose_view(session, self.new_date_selected,
                                            title="בחרת בתאריך שכבר עבר. בחר שוב").draw()
            return

        app_day = get_new_appointment_day(date)

        app_day.save()
        self.ui.create_text_view(session, "היום סומן כיום שיש בו תורים").draw()

    def view_my_appointments(self, session: Session):
        self.ui.clear(session)
        buttons = []
        for app in DoctorAppointment.objects(patient=session.user):
            buttons.append(Button(app.to_string(), lambda s, a=app: self.select_appointment(session, a)))
        if len(buttons) == 0:
            text = "אין לך תורים לרופא"
        else:
            text = "לחץ על תור לפעולות נוספות"
        buttons.append(Button("🔙", lambda s: self.main(s)))
        self.ui.create_button_group_view(session, text, buttons).draw()

    def select_appointment(self, session: Session, app: DoctorAppointment):
        self.ui.clear(session)

        def delete_appointment():
            app.patient = None
            app.save()
            self.ui.summarize_and_close(session, [self.ui.create_text_view(session, "התור בוטל")])

            # delete reminder
            remove_by_rule(lambda job: job.kwargs.get('appointment_time') == app.time)

        buttons = [
            Button("בטל את התור", lambda s: delete_appointment()),
            Button("חזרה", self.view_my_appointments),
        ]

        self.ui.create_button_group_view(session, "מה ברצונך לעשות עם התור?", buttons).draw()

    def make_appointment(self, session: Session):
        self.ui.clear(session)
        buttons = []
        for d in DoctorAppointmentDay.objects(date__gt=datetime.date.today()):
            buttons.append(Button(d.date.strftime("%d/%m/%Y"), lambda s, dd=d: self.date_selected(s, dd)))
        buttons.append(Button("🔙", lambda s: self.main(s)))
        self.ui.create_button_group_view(session, "בחר תאריך", buttons).draw()

    def date_selected(self, session: Session, day: DoctorAppointmentDay):
        self.ui.clear(session)
        available_slots = []
        for app in day.appointments:
            if app.patient is None or 'patient' not in app:
                available_slots.append(Button(app.to_string(), lambda s, app=app: self.slot_selected(session, app)))
            else:
                print("appointment is taken in time ", app.time)

        if len(available_slots) == 0:
            buttons = []
            for d in DoctorAppointmentDay.objects(date__gt=datetime.date.today()):
                buttons.append(Button(d.date.strftime("%d/%m/%Y"), lambda s, dd=d: self.date_selected(s, dd)))
            self.ui.create_button_group_view(session, "כל התורים בתאריך הזה נתפסו, אנא בחר תאריך אחר", buttons).draw()
            return

        available_slots.append(Button("🔙", lambda s: self.main(s)))
        self.ui.create_text_view(session, "יש תורים פנויים ביום הזה").draw()
        self.ui.create_button_group_view(session, "בחר סלוט", available_slots).draw()

    def slot_selected(self, session: Session, app: DoctorAppointment):
        self.ui.clear(session)
        app.patient = session.user
        app.save()
        self.ui.summarize_and_close(session, [self.ui.create_text_view(session, "נרשמת לסלוט רופא בהצלחה")])
        # The day before, at 10 PM
        scheduled_time = datetime.datetime.fromordinal(app.time.toordinal()) - datetime.timedelta(hours=2)
        # scheduled_time = datetime.datetime.now() + datetime.timedelta(seconds=4) # in four seconds
        self.schedule_job(scheduled_time, appointment_time=app.time)


    def get_summarize_views(self, session: Session) -> [View]:
        """
        Called externally when the BotManager wants to close this feature.
        This function returns an array of views that summarize the current
        status of the session. The array can be empty.
        :param session: Session object
        :return: Array of views summarizing the current feature Status.
        """
        pass

    def is_authorized(self, user: User) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        return "מתלם" in user.role

    def get_scheduled_jobs(self) -> [ScheduledJob]:
        """
        Get jobs (scheduled functions) that need to be called at specific times.
        :return: List of Jobs that will be created and called.
        """
        return []

    def scheduled_jobs_parser(self, appointment_time=None):
        if appointment_time is None:
            return
        # set reminder
        appointment = DoctorAppointment.objects(time=appointment_time)[0]
        self.remind_appointment(appointment)

    def remind_appointment(self, appointment: DoctorAppointment):
        if appointment.patient is None:
            return False
        appointment_user: User = appointment.patient
        new_session = self.ui.create_session("remind_appointment", appointment_user)
        text = f"שלום {appointment_user.name}\n" \
               f"מזכירים לך שקבעת תור לרופא: {appointment.to_string()}.\n" \
               f"נא לא לאחר"
        self.ui.create_text_view(new_session, text).draw()
        return True

    def remind_all_appointments(self, session: Session):
        count = 0
        for appointment in DoctorAppointment.objects(time__gt=datetime.date.today(),
                                                     time__lt=datetime.date.today() + datetime.timedelta(days=1)):
            if self.remind_appointment(appointment):
                count += 1
        self.ui.clear(session)
        self.ui.summarize_and_close(session, [self.ui.create_text_view(session, f"נשלחו {count} תזכורות")])

    def return_to_menu(self, session: Session):
        HierarchicalMenu.run_menu(self.ui, session.user)
