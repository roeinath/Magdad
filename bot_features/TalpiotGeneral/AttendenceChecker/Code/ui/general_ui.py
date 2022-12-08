from typing import Callable, Any

from APIs.TalpiotAPIs.AttendanceChecker.state import State
from bot_features.TalpiotGeneral.AttendenceChecker.Code.logic.attendance_cadet_data import AttendanceCadetData
from bot_framework.ui.button import Button


def get_user_button(callback_func: Callable[[AttendanceCadetData], Any], cadet: AttendanceCadetData):
    """
    Generates a single button for given cadet
    :param callback_func: Callback function for updating a cadet's state
    :param cadet: The cadet who's name will be written on the button, and their state will be updated by it
    :return: The button
    """
    template = '{color}\t{name}'
    color_map = {State.HERE: '\U0001F535', State.NO: '\U0001F534', State.OMW: '\u26AB'}
    text = template.format(color=color_map[cadet.state], name=cadet.session.user.name)

    def callback(session):
        cadet.state = cadet.state.next()
        callback_func(cadet)

    return Button(text, callback)
