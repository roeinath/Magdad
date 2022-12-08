from APIs.TalpiotAPIs import *
from APIs.TalpiotAPIs.mahzors_utils import get_mahzor_year_3
from bot_features.Shagmach.ParkingSystem.Logic.ParkingSystemLogic import *
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.session import Session
from bot_framework.ui.button import Button
from bot_framework.ui.ui import UI


class ParkingSystem(BotFeature):
    def __init__(self, ui: UI):
        super().__init__(ui)

    def main(self, session: Session):
        self.ui.create_text_view(session, "נא הכנס מספר רכב 🔢").draw()
        self.ui.get_text(session, self.issue_permit_for_car_number)

    def issue_permit_for_car_number(self, session, car_licence_plate):
        car_licence_plate = car_licence_plate.replace('-', '')
        today_date = datetime.datetime.today()
        tomorrow_date = today_date + datetime.timedelta(days=1)
        buttons: [Button] = [
            self.ui.create_button_view("היום", lambda s: self.issue_permit(s, car_licence_plate, today_date)),
            self.ui.create_button_view("מחר", lambda s: self.issue_permit(s, car_licence_plate, tomorrow_date)),
        ]
        self.ui.create_button_group_view(session, 'למתי האישור כניסה? 🕒', buttons).draw()

    def issue_permit(self, session, car_licence_plate, date):
        loading_text = self.ui.create_text_view(session, 'מנפיק אישור.. 🚗')
        loading_text.draw()

        result = ParkingSystemLogic.issue_permit(
            car_licence_plate,
            date,
            session.user.get_first_name(),
            session.user.get_last_name(),
            session.user.phone_number,
            session.user.email
        )

        loading_text.remove()

        self.ui.create_text_view(session, result).draw()

        buttons = [
            self.ui.create_button_view("אישור נוסף לרכב הזה 🔂",
                                       lambda s: self.issue_permit_for_car_number(s, car_licence_plate)),
            self.ui.create_button_view("אישור נוסף לרכב אחר 🔁", lambda s: self.main(s)),
            self.ui.create_button_view("סיימתי תודה", lambda s: self.ui.summarize_and_close(s, [
                self.ui.create_text_view(session, result)]))
        ]

        self.ui.create_button_group_view(session, 'מה עכשיו?', buttons).draw()

    def is_authorized(self, user: User) -> bool:
        return user.mahzor <= get_mahzor_year_3().mahzor_num
