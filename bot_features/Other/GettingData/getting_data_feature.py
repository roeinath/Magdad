from bot_framework import *
from APIs.ExternalAPIs import *
from APIs.TalpiotAPIs import *
from APIs.Database import *
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.ui import UI
from APIs.TalpiotAPIs.AssessmentAPI.tsyunomat import main
import hashlib
import pandas as pd
from APIs.TalpiotAPIs.AssessmentAPI.Database import login_info
from APIs.TalpiotAPIs.AssessmentAPI.tsyunomat import GetDataFromDB
from APIs.TalpiotAPIs.User.user import User

SHA1_MADAR_PASSWORD = 'ea18f29e22c1c108ef6799437e6ee60a7340df22'
ENTER_CADET_ENTRY_DETAILS = 'הכנס פרטי התחברות של צוערים✍️'
PULL_CADET_GRADES = 'משוך ציוני צוערים💪'
SWITCH_MADAR_PASSWORD = 'החלף מפתח למשיכת נתונים♻️'
DELETE_CADET_ENTRY_DETAILS = 'מחק פרטי התחברות של צוערים🗑'


class GettingDataFeature(BotFeature):
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
        self.ui.create_text_view(session, "הכנס סיסמא לפיצ'וער: ").draw()
        self.ui.get_text(session, self.lobby_feature)

    def lobby_feature(self, session: Session, madar_password: str):
        """
        the security ate for pulling the cadets grades with password and encryption key
        :param session: Session object
        :param fernet_key: special key for encrypting and decrypting the cadets entry details
        :param madar_password: password to have access to pull the cadets grades
        :return: True if correct password entered, False otherwise
        """
        if hashlib.sha1(bytes(madar_password, encoding='utf8')).hexdigest() != SHA1_MADAR_PASSWORD:
            self.ui.create_text_view(session, "סיסמא שגויה, לא ניתן למשוך נתונים").draw()
            self.ui.get_text(session, self.send_text_back_to_usr)
        else:
            self.ui.clear(session)
            buttons = [self.ui.create_button_view(ENTER_CADET_ENTRY_DETAILS, lambda s: self.get_entry_excel(s)),
                       self.ui.create_button_view(PULL_CADET_GRADES, lambda s: self.get_fernet_key(s)),
                       self.ui.create_button_view(SWITCH_MADAR_PASSWORD, lambda s: self.get_old_and_new_key(s)),
                       self.ui.create_button_view(DELETE_CADET_ENTRY_DETAILS, lambda s: self.get_names_to_delete(s)),
                       self.get_exit_button()]
            self.ui.create_button_group_view(session, 'תפריט:', buttons).draw()

    def get_fernet_key(self, session: Session):
        """
        getting and sending the key to pull data
        :param session: Session object
        :return:
        """
        self.ui.create_text_view(session, "הכנס מפתח למשיכת ציוני הצוערים: ").draw()
        self.ui.get_text(session, self.pull_grades)

    def pull_grades(self, session: Session, madar_password: str):
        """
        using the fernet_key, pulling the entry cadet's data and their grades
        :param session: Session object
        :param madar_password: the fernet_key passed from the user
        :return: a message if the process was successful or not
        """
        self.ui.create_text_view(session, "הנתונים נמשכים כעת, פעולה זו עשויה להימשך מספר דקות...").draw()
        self.ui.get_text(session, self.send_text_back_to_usr)
        flag = main.start(madar_password)
        if False in list(flag.values()) or 'entry details' in list(flag.values()):
            key_list = list(flag.keys())
            txt_table = "סיכום בעיות: \n"
            for student in key_list:
                if flag[student] == 'entry details':
                    txt_table += student + "- נתוני כניסה שגויים\n"
                if not flag[student]:
                    txt_table += student + "- סיבה לא ידועה\n"

            txt_table.strip()
            self.ui.create_text_view(session, txt_table).draw()
            self.ui.get_text(session, self.send_text_back_to_usr)
        else:
            self.ui.create_text_view(session, "הנתונים נמשכו בהצלחה ואוחסנו במאגר הנתונים").draw()
            self.ui.get_text(session, self.send_text_back_to_usr)

    def get_entry_excel(self, session: Session):
        """
        getting and sending the key and the path to the excel with the data
        :param session: Session object
        :return:
        """
        self.ui.create_text_view(session, "הכנס מפתח פסיק(,) ומסלול לקובץ עם פרטי הצוערים: ").draw()
        self.ui.get_text(session, self.enter_cadet_details)

    def enter_cadet_details(self, session: Session, excel_data: str):
        """
        parsing the excel and entering the data to DB using the key
        :param session: Session object
        :param excel_data: key and path to file
        :return:
        """
        key_and_path = excel_data.split(",")
        key = key_and_path[0]
        path = key_and_path[1]
        df = pd.read_excel(path)
        cadets_user_list = User.objects.filter()
        cadets_name_list = []
        for user in cadets_user_list:
            cadets_name_list.append(user.name)
        data = {}
        inputs = [x for x in df.itertuples()]
        # name list of matlam and cmp to names in excel
        for row in inputs:
            if row[1] not in cadets_name_list:
                print(row[1])
                self.ui.create_text_view(session, " השם " + row[1] + " לא תואם את השם בתלפיאיקס ").draw()
                continue
            data[row[1]] = {'mahzor': str(row[2]), 'email': str(row[3]), 'password': str(row[4]), 'cse_username': str(row[5]), 'cse_password': str(row[6])}
        for cadet in list(data.keys()):
            login_info.insert(cadet, data[cadet]['mahzor'], data[cadet]['email'], data[cadet]['password'], data[cadet]['cse_username'],
                              data[cadet]['cse_password'], key)
        self.ui.create_text_view(session, "פרטי ההתחברות של הצוערים הוצפנו ואוחסנו בהצלחה ").draw()

    def get_old_and_new_key(self, session: Session):
        """
        getting from the user and sending the old password
        you want to replace and the new password
        :param session: Session object
        :return:
        """
        self.ui.create_text_view(session, "הכנס את המפתח הישן רווח ומפתח חדש: ").draw()
        self.ui.get_text(session, self.change_madar_password)

    def change_madar_password(self, session: Session, old_and_new_password: str):
        """
        changing the key
        :param old_and_new_password: the old password and the new password
        :param session: Session object
        :return: a message to the user
        """
        keys = old_and_new_password.split(" ")
        old_madar_password = keys[0]
        new_madar_password = keys[1]
        data = GetDataFromDB.get_users_info(old_madar_password)
        for cadet in list(data.keys()):
            login_info.delete(cadet, data[cadet]['mahzor'])
        for cadet in list(data.keys()):
            login_info.insert(cadet,data[cadet]['mahzor'],data[cadet]['email'], data[cadet]['password'], data[cadet]['cse_username'],
                              data[cadet]['cse_password'], new_madar_password)
        self.ui.create_text_view(session, "המפתח הוחלף בהצלחה ").draw()

    def get_names_to_delete(self, session):
        """
        get from the bot names wish to delete
        :param session: Session object
        :return:
        """
        self.ui.create_text_view(session, "כתוב שמות של צוערים (שם של צוער מקף מספר מחזור פסיק) שאותם תרצה למחוק: ").draw()
        self.ui.get_text(session, self.delete_cadet_details)

    def delete_cadet_details(self, session: Session, cadets_names: str):
        """
        deletes all login_info connected to the names in the strings
        :param session:
        :param cadets_names:
        :return:
        """
        cadets_names_list = cadets_names.split(",")
        for cadet_name in cadets_names_list:
            tmp = cadet_name.split("-")
            login_info.delete(tmp[0], tmp[1])
        self.ui.create_text_view(session, "פרטי הצוערים נמחקו בהצלחה ").draw()

    def is_authorized(self, user: User) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        return user.name in ['רום פייביש', 'שחר יוסף זכריה', 'מדר תלפיות', 'יהלי אקשטיין', 'יואב פלטו', 'אלון קגן',
                             'עומר ישראלי']

    def send_text_back_to_usr(self, session, usr_string):
        self.ui.create_text_view(session, usr_string).draw()

    def get_exit_button(self):
        # Creates 'back' buttons for all screens
        return self.ui.create_button_view("🔙", lambda s: self.return_to_menu(s))

    def return_to_menu(self, session: Session):
        from bot_features.SystemFeatures.HierarchicalMenu.Code.hierarchical_menu import \
            HierarchicalMenu
        self.ui.clear(session)
        HierarchicalMenu.run_menu(self.ui, session.user)
