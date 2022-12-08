from APIs.TalpiotAPIs.AttendanceChecker.state import State
from bot_framework.View.button_group_view import ButtonGroupView
from bot_framework.session import Session


class AttendanceCadetData:
    def __init__(self, user_session: Session, current_view: ButtonGroupView, state: State = State.OMW):
        self.state: State = state
        self.session: Session = user_session
        self.current_view: ButtonGroupView = current_view
