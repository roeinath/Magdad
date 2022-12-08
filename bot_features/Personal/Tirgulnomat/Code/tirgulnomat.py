from bot_features.Personal.Tirgulnomat.Code.Targan import *
from APIs.ExternalAPIs import *
from APIs.TalpiotAPIs import *
from bot_features.Personal.Tirgulnomat.Code.group_utils import *

from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.ui import UI

import hashlib

TIRGULNOMAT = "תרגולנומט"
ARE_YOU_SURE = "האם את/ה בטוח/ה שאת/ה רוצה להוסיף תרגול נוסף? פעולה זו נעשית על ידי מפקד/ת הצוות."
ENTER_NEW_TARGAN = "🚨 הזנת תרגול נוסף"
ENTER_TARGAN_COUNT = "שלח/י הודעה עם כמות התרגולים הנוספים שברצונך להוסיף:"
TRY_AGAIN = "נסה/י שוב."
SHOW_TARGANS_STATUS = "👀 הצגת סטטוס תרגול נוסף"
SHOW_DAILY_HET = "🕖 הצגת צוערי ח׳ יומית ונהלי דיגום"
SIGN_A_MISHMAAT = "✍️ החתמת א׳ משמעת"
SIGN_DIVISION_COMMANDER = "✍️ החתמת מ״מ"
NO_CHECKED_TARGANS = "אין לך תרגולים נוספים המחכים לבדיקת מ״מ"
NO_UNCHECKED_TARGANS = "אין לך תרגולים נוספים המחכים לבדיקת א׳ משמעת"
ENTER_PASSWORD = "הכנסת סיסמה:"
SUCCESSFULLY_SIGNED = "הוחתם בהצלחה"
SHOW_SUBORDINATES = "🚔הצגת סטטוס פקודים"
WRONG_PASSWORD = "הסיסמה שהוכנסה שגויה"
EXIT = "חזרה אחורה"
DIGUM_REQUIREMENTS = "יש לבדוק:\n• חוגר\n• פנקס שבי\n• דסקית\n• תקניות מדים\n• נעליים\n• גרביים\n• אישור זקן\n• גילוח\n• צחצוח\n• תספורת\n• אחר"
FINISH_PASSWORD = "סיום הכנסת סיסמה"

DIVISION_COMMANDER_PASSWORD = "4dea5c7cb70f50322ec9d734aa4aa078be9227c05251e18991c596f387552370"
A_MISHMAAT_PASSWORD = "748064be03a08df81e31bd6f9e7e7c4cc9f84b4401b9a3c6e85b7ff816d3ba68"


class Tirgulnomat(BotFeature):
    guess = {}  # This dictionary holds the current password guess of every user, where the key is their session's ID
    password_text_view = {}

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)

    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """
        u: User = User.get_by_telegram_id(session.user.telegram_id)
        subordinates = get_subordinates_by_commander(u)
        # print(f'{u.name}: {[s.name for s in subordinates]}')
        is_team_commander = subordinates != []
        is_allowed_a_mishmaat = u.mahzor <= 42
        buttons = [self.ui.create_button_view(ENTER_NEW_TARGAN, lambda s: self.request_new_targan(s)),
                   self.ui.create_button_view(SHOW_TARGANS_STATUS, lambda s: self.show_targan_status(s)),
                   self.ui.create_button_view(SIGN_A_MISHMAAT,
                                              lambda s: self.sign_targan(s, Responsible.A_MISHMAAT)),
                   self.ui.create_button_view(SIGN_DIVISION_COMMANDER,
                                              lambda s: self.sign_targan(s, Responsible.DIVISION_COMMANDER))]
        if is_team_commander:
            buttons.append(self.ui.create_button_view(SHOW_SUBORDINATES,
                                                      lambda s: self.show_status_table(s, subordinates)))
        if is_allowed_a_mishmaat:
            buttons.append(self.ui.create_button_view(SHOW_DAILY_HET, lambda s: self.print_a_mishmaat_data(s)))
        buttons.append(self.get_exit_button())
        self.ui.create_button_group_view(session, TIRGULNOMAT, buttons).draw()

    def show_status_table(self, session, subordinates):
        messages_per_subordinate = []
        for s in subordinates:
            unchecked_targans, unsigned_targans, signed_targans = self.get_user_targans_by_type(s)
            t = f'•ל{s.name} נותרו {len(unchecked_targans)} תרגולים נוספים שעוד לא נבדקו ו־{len(unsigned_targans)} שעוד לא הוחתמו ע״י מ״מ.'
            messages_per_subordinate.append(t)
        final_message = '\n'.join(messages_per_subordinate)
        self.ui.create_text_view(session, final_message).draw()
        self.ui.create_button_group_view(session, EXIT, [self.get_exit_button()]).draw()

    def request_new_targan(self, session):
        buttons = [self.ui.create_button_view("✅", lambda s: self.request_targan_count(s)),
                   self.ui.create_button_view("❌", lambda s: self.return_to_menu(s))]
        self.ui.create_button_group_view(session, ARE_YOU_SURE, buttons).draw()

    def request_targan_count(self, session):
        self.ui.create_text_view(session, ENTER_TARGAN_COUNT).draw()
        self.ui.get_text(session, self.got_targan_count)

    def got_targan_count(self, session, num: str):
        while not num.isdigit():
            self.ui.create_text_view(session, TRY_AGAIN).draw()
            self.ui.get_text(session, self.got_targan_count)
            return

        n = int(num)
        buttons = [self.ui.create_button_view("✅", lambda s: self.add_targans(s, n)),
                   self.ui.create_button_view("❌", lambda s: self.return_to_menu(s))]
        self.ui.create_button_group_view(session, "האם את/ה בטוח שאת/ה רוצה להוסיף " + num + " תרגולים נוספים?", buttons) \
            .draw()

    def add_targans(self, session, n):
        for i in range(n):
            self.save_new_targan(User.get_by_telegram_id(session.user.telegram_id))

        self.ui.create_text_view(session, f"התווספו {n} תרגולים נוספים.").draw()
        self.ui.create_button_group_view(session, EXIT, [self.get_exit_button()]).draw()

    def save_new_targan(self, cadet):
        # Sends message about new targan, creates one and saves it
        # self.ui.create_text_view(session, ADDED_TARGAN_FOR + cadet.name).draw()
        t = Targan(user=cadet, status=TarganStatus.UNCHECKED, date_given=datetime.datetime.today())
        t.save()

    def show_targan_status(self, session):
        # Print out the status of user's targans
        u: User = User.get_by_telegram_id(session.user.telegram_id)
        unchecked_targans, unsigned_targans, signed_targans = self.get_user_targans_by_type(u)
        text = f'נותרו לך ' \
               f'{len(unchecked_targans)}' \
               f' תרגולים נוספים שאינם נבדקו ע״י א׳ משמעת, ו־' \
               f'{len(unsigned_targans)}' \
               f' תרגולים נוספים שהמ״מ עדיין לא חתמ/ה עליהם.'
        self.ui.create_text_view(session, text).draw()
        self.ui.create_button_group_view(session, EXIT, [self.get_exit_button()]).draw()

    def print_a_mishmaat_data(self, session):
        # Lists out all cadets with targans still unchecked, and lets A' mishmaat check them
        u = User.get_by_telegram_id(session.user.telegram_id)
        # TODO: Better permission management
        self.ui.create_text_view(session, DIGUM_REQUIREMENTS).draw()
        users = Targan.get_all_users_with_unchecked_targans()
        list_of_names = '\n'.join([f'• {user.name}' for user in users])
        text_to_show = f'צוערים עם תרגולים נוספים שעדיין לא נבדקו ע״י א׳ משמעת:\n{list_of_names}'
        self.ui.create_text_view(session, text_to_show).draw()
        self.ui.create_button_group_view(session, EXIT, [self.get_exit_button()]).draw()

    def sign_targan(self, session, who):
        u = User.get_by_telegram_id(session.user.telegram_id)
        unchecked_targans, unsigned_targans, signed_targans = self.get_user_targans_by_type(u)
        targan_type_to_check = None
        no_relevant_targans_message = None
        if who == Responsible.A_MISHMAAT:
            targan_type_to_check = unchecked_targans
            no_relevant_targans_message = NO_UNCHECKED_TARGANS
        elif who == Responsible.DIVISION_COMMANDER:
            targan_type_to_check = unsigned_targans
            no_relevant_targans_message = NO_CHECKED_TARGANS
        else:
            raise Exception("Invalid 'who' type")

        if len(targan_type_to_check) == 0:
            self.ui.create_text_view(session, no_relevant_targans_message).draw()
            self.ui.create_button_group_view(session, EXIT, [self.get_exit_button()]).draw()
            return

        self.password_text_view[session.user.telegram_id] = self.ui.create_text_view(session, "")
        self.password_text_view[session.user.telegram_id].draw()
        self.create_button_pad(session, who)

    def check_password_and_sign(self, session, who):
        u = User.get_by_telegram_id(session.user.telegram_id)
        unchecked_targans, unsigned_targans, signed_targans = self.get_user_targans_by_type(u)
        password_to_check = None
        if who == Responsible.A_MISHMAAT:
            password_to_check = A_MISHMAAT_PASSWORD
        elif who == Responsible.DIVISION_COMMANDER:
            password_to_check = DIVISION_COMMANDER_PASSWORD
        else:
            raise Exception("Invalid 'who' type")
        given_password = ''.join([str(d) for d in self.guess[session.user.telegram_id]])
        hashed_given_password = hashlib.sha256(given_password.encode('utf-8')).hexdigest()

        if hashed_given_password == password_to_check:
            # A' Mishmaat signs only one targan, DC signs all remaining targans
            if who == Responsible.A_MISHMAAT:
                targan = unchecked_targans[0]
                targan.status = TarganStatus.UNSIGNED
                targan.date_signed_by_a_mishmaat = datetime.datetime.today()
                targan.save()
            elif who == Responsible.DIVISION_COMMANDER:
                for targan in unsigned_targans:
                    targan.status = TarganStatus.SIGNED
                    targan.date_signed_by_division_commander = datetime.datetime.today()
                    targan.save()

            self.ui.clear(session)
            self.ui.summarize_and_close(session, [self.ui.create_text_view(session, SUCCESSFULLY_SIGNED)])
        else:
            self.ui.clear(session)
            self.ui.create_text_view(session, WRONG_PASSWORD).draw()
            self.guess[session.user.telegram_id] = []
            self.ui.create_button_group_view(session, EXIT, [self.get_exit_button()]).draw()
        return

    # TODO: Don't go all the way back up?
    def get_exit_button(self):
        # Creates 'back' buttons for all screens
        return self.ui.create_button_view("🔙", lambda s: self.return_to_menu(s))

    def create_button_pad(self, session, who):
        # Creates password keypad
        buttons = self.get_number_pad(session)
        buttons.append([self.ui.create_button_view(FINISH_PASSWORD, lambda s: self.check_password_and_sign(s, who))])

        self.password_text_view[session.user.telegram_id] = self.ui.create_text_view(session, "")
        self.password_text_view[session.user.telegram_id].draw()
        self.ui.create_button_matrix_view(session, "הכנס/י סיסמה", buttons).draw()

    def get_number_pad(self, session):
        def update_text():
            self.password_text_view[session.user.telegram_id].update(''.join(self.guess[session.user.telegram_id]))

        def add_digit(digit):
            self.guess[session.user.telegram_id].append(str(digit))
            update_text()

        def remove_digit():
            if self.guess[session.user.telegram_id]:
                self.guess[session.user.telegram_id].pop()
            update_text()

        buttons = []
        self.guess[session.user.telegram_id] = []
        for i in range(3):
            b = []
            for j in range(3):
                k = 3 * i + j + 1
                b.append((lambda x: self.ui.create_button_view(str(x), lambda s: add_digit(x)))(k))
            buttons.append(b)
        buttons.append([
            self.ui.create_button_view("DEL", lambda s: remove_digit()),
            self.ui.create_button_view("0", lambda s: add_digit(0)),
            self.ui.create_button_view("", lambda s: None),
        ])
        return buttons

    def get_user_targans_by_type(self, user):
        # Returns user's targans grouped by status
        targans = Targan.get_all_targans_per_user(user)
        unchecked_targans = list(filter(lambda t: t.status == TarganStatus.UNCHECKED, targans))
        unsigned_targans = list(filter(lambda t: t.status == TarganStatus.UNSIGNED, targans))
        signed_targans = list(filter(lambda t: t.status == TarganStatus.SIGNED, targans))

        return unchecked_targans, unsigned_targans, signed_targans

    def return_to_menu(self, session: Session):
        from bot_features.SystemFeatures.HierarchicalMenu.Code.hierarchical_menu import \
            HierarchicalMenu
        self.ui.clear(session)
        HierarchicalMenu.run_menu(self.ui, session.user)

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
