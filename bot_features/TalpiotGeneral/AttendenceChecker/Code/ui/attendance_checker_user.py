from APIs.TalpiotAPIs.AttendanceChecker.state import State
from APIs.TalpiotAPIs.User.user import User
from bot_features.TalpiotGeneral.AttendenceChecker.Code.logic.attendance_cadet_data import AttendanceCadetData
from bot_features.TalpiotGeneral.AttendenceChecker.Code.logic.attendance_data import AttendanceData
from bot_features.TalpiotGeneral.AttendenceChecker.Code.ui.general_ui import get_user_button
from bot_framework.ui.ui import UI


class AttendanceCheckerUser(object):
    def __init__(self, ui: UI):
        self.ui: UI = ui

    def start_user_checker(self, data: AttendanceData, user: User):
        user_session = self.ui.create_session('attendance', user)
        user_session.data = data
        state = State.OMW
        if data.scheduled_checker is not None:
            state = State.NO if data.scheduled_checker.get_missing_reason_if_exists(user) else State.OMW
        data.add_member_session(user_session, state)

    def update_view(self, user: AttendanceCadetData):
        for admin in user.session.data.admins:
            if admin.session.user == user.session.user:
                return

        def update_callback(data: AttendanceCadetData):
            for admin in user.session.data.admins:
                user.session.data.admin_manager.update_view(admin)
            self.update_view(data)

        msg_text = "וידוא נוכחות עבור " + user.session.data.name
        msg_buttons = [get_user_button(update_callback, user)]

        if user.current_view is None:
            user.current_view = self.ui.create_button_group_view(user.session, msg_text, msg_buttons)
            user.current_view.draw()
        else:
            user.current_view.update(new_text=r'וידוא נוכחות בתהליך...', new_buttons=msg_buttons)
