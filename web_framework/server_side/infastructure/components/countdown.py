from datetime import datetime

from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent


class CountDown(UIComponent):
    def __init__(self, time: datetime):
        super().__init__()
        self.__time = time

    def render(self):
        return {
            JSON_TYPE: 'CountDown',
            JSON_ID: self.id,
            JSON_TIME: self.__time
        }

    def update_time(self, time):
        self.__time = time
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {
                JSON_ID: self.id,
                JSON_TIME: self.__time
            }
        })
