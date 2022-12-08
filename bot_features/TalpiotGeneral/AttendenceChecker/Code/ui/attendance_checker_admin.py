from APIs.TalpiotAPIs.AttendanceChecker.state import State
from APIs.TalpiotAPIs.Group import *
from APIs.TalpiotAPIs.User.user import User
from bot_features.TalpiotGeneral.AttendenceChecker.Code.logic.attendance_cadet_data import AttendanceCadetData
from bot_features.TalpiotGeneral.AttendenceChecker.Code.logic.attendance_data import AttendanceData
from bot_features.TalpiotGeneral.AttendenceChecker.Code.ui.general_ui import get_user_button
from bot_framework.Commands.general_bot_commands import simple_send_message
from bot_framework.session import Session
from bot_framework.ui.button import Button
from bot_framework.ui.ui import UI


class AttendanceCheckerAdmin(object):
    def __init__(self, ui: UI):
        self.ui: UI = ui

    def start_admin_checker(self, data: AttendanceData, user: User):
        user_session = self.ui.create_session('attendance', user)

        user_session.data = data
        state = State.OMW
        if data.scheduled_checker is not None:
            state = State.NO if data.scheduled_checker.get_missing_reason_if_exists(user) else State.OMW
        data.add_admin_session(user_session, state)

    def get_buttons(self, session):
        def update_callback(updated_user: AttendanceCadetData):
            if updated_user not in session.data.admins:
                session.data.user_manager.update_view(updated_user)
            for admin in session.data.admins:
                self.update_view(admin)

        def sort_callback(session: Session) -> None:
            session.data.members.sort(key=AttendanceData.key_func)
            session.data.admins.sort(key=AttendanceData.key_func)
            for admin in session.data.admins:
                self.update_view(admin)

        def close_callback(session: Session):
            session.data.closed = True
            for user in session.data.members:
                self.ui.summarize_and_close(user.session, [])
            users_in_group = [user.session.user for user in session.data.members]

            groups_to_send_summary = set(CommandedGroup.objects(participants__in=users_in_group))
            for commanded_group in groups_to_send_summary:
                commander: User = commanded_group.commander
                group_summary = f"הודעה שנשלחת ל{commanded_group.name}\n{session.data.get_summary(commanded_group)}"
                simple_send_message(self.ui, {'user_list': [commander], 'text': group_summary})

            admin_summary = session.data.get_summary()
            for admin in session.data.admins:
                self.ui.summarize_and_close(admin.session, [self.ui.create_text_view(admin.session, admin_summary)])

        def alert_cadets_callback(session: Session):
            cadet_to_alert = [user.session.user for user in session.data.members if user.state == State.OMW]
            simple_send_message(self.ui, {'user_list': cadet_to_alert, 'text': 'לוד"צ!'})
            return

        buttons = [get_user_button(update_callback, cadet) for cadet in session.data.members]
        buttons.append(Button('סדר את הרשימה', sort_callback))
        buttons.append(Button("סגור וידוא נוכחות", close_callback))
        buttons.append(Button("להציק", alert_cadets_callback))
        return buttons

    def update_view(self, user: AttendanceCadetData):
        msg_text = f"וידוא נוכחות (מצב חנתר) עבור {user.session.data.name}"
        msg_buttons = self.get_buttons(user.session)

        if user.current_view is None:
            user.current_view = self.ui.create_button_group_view(user.session, msg_text, msg_buttons)
            user.current_view.draw()
        else:
            user.current_view.update(new_text=f'וידוא נוכחות עבןר {user.session.data.name} בתהליך...',
                                     new_buttons=msg_buttons)
