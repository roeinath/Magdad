from bot_framework.session import Session
from bot_features.Mahzori.Vidutz.Code.state import State


class VidutzCadetData:
    def __init__(self, user_session: Session, state: State = State.OMW):
        self.state: State = state
        self.session: Session = user_session
