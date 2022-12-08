from typing import List, Callable, Optional, Any, Tuple

from bot_framework.session import Session
from bot_framework.ui.ui import UI, Button
from bot_features.Mahzori.Vidutz.Code.state import State
from bot_features.Mahzori.Vidutz.Code.vidutz_cadet_data import VidutzCadetData


class VidutzData:
    def __init__(self, founder_session: Session, ui: UI):
        """
        Create a new VidutzData instance to manage a single vidutz
        :param founder_session: Session object of initiating hantar
        """
        self.ui: UI = ui
        self.hapash_children: List[VidutzCadetData] = list()
        self.hantar_children: List[VidutzCadetData] = list()
        self.all_children: List[VidutzCadetData] = list()
        self.add_hantar(founder_session, state=State.HERE)

    def add_hapash(self, hapash_session: Session) -> None:
        """
        Add a hapash to the vidutz's cadet list
        :param hapash_session: Session object of added hapash
        """
        new_data = VidutzCadetData(hapash_session)
        self.hapash_children += [new_data]
        self.all_children += [new_data]

    def add_hantar(self, hantar_session: Session, state: State = State.OMW) -> None:
        """
        Add a hantar to the vidutz's cadet list
        :param hantar_session: Session object of added hantar
        :param state: Default state for this hantar (usually HERE for initiator and OMW otherwise)
        """
        new_data = VidutzCadetData(hantar_session, state=state)
        self.hantar_children += [new_data]
        self.all_children += [new_data]

    def sort(self) -> None:
        """
        Sorts the children lists by state and name
        """
        self.hapash_children.sort(key=VidutzData.key_func)
        self.hapash_children.sort(key=VidutzData.key_func)
        self.all_children.sort(key=VidutzData.key_func)

    def get_buttons(self, update_callback: Callable[[VidutzCadetData, State], Any],
                    cadet: VidutzCadetData,
                    close_callback: Optional[Callable[[None], Any]] = None,
                    sort_callback: Optional[Callable[[None], Any]] = None,
                    hantar: bool = False):
        """
        Returns all of the reply keyboard buttons for a cadet. Returns a hantar keyboard iff hantar flag is set to True
        - in such case close_callback and sort_callback must not be None. Returns keyboard for given (non-None) cadet
        otherwise.
        :param cadet: The hapash whom the keyboard is to be sent to. Leave None for a hantar keyboard.
        :param update_callback: Callback function for updating a cadet's state
        :param close_callback: Callback function for the close button
        :param sort_callback: Callback function for the sort button - only has to refresh relevant Views
        :param hantar: True for hantar keyboard
        :return: All of the reply keyboard buttons for given input.
        """
        # cadet_list = sorted(self.hantar_children + self.hapash_children, key=VidutzData.key_func)
        cadet_list = self.all_children
        if hantar:
            buttons = [self._get_single_button(update_callback, cadet) for cadet in cadet_list]

            def callback(session: Session) -> None:
                self.sort()
                sort_callback(session)

            order_button = Button('סדר את הרשימה', callback)
            buttons += [order_button]
            # if self._get_num_checked() == len(self.all_children):
            close_button = self._get_close_button(cadet, close_callback)
            buttons += [close_button]
            return buttons
        else:
            user_list = cadet.session.user.get_team()
            return [self._get_single_button(update_callback, cadet) for cadet in cadet_list if
                    (cadet.session.user in user_list)]

    def _get_single_button(self, callback_func: Callable[[VidutzCadetData, State], Any],
                           cadet: VidutzCadetData):
        """
        Generates a single button for given cadet
        :param callback_func: Callback function for updating a cadet's state
        :param cadet: The cadet who's name will be written on the button, and their state will be updated by it
        :return: The button
        """
        template = '{color}\t{name}'
        color_map = {State.HERE: '\U0001F535', State.NO: '\U0001F534', State.OMW: '\u26AB'}
        text = template.format(color=color_map[cadet.state], name=cadet.session.user.get_short_name())
        return Button(text, lambda test: callback_func(cadet, cadet.state.next()))

    def _get_close_button(self, cadet: VidutzCadetData,
                          close_callback: Callable[[None], Any]):
        close_text = f'סיום וידו"צ ({self._get_num_checked()} סומנו)'
        return Button(close_text, lambda session: close_callback(session))

    def _get_num_checked(self) -> int:
        """
        Returns the count of cadets who are checked in the list (i.e. their state is not OMW)
        :return: The count of cadets who are checked in the list (i.e. their state is not OMW)
        """
        cadet_list = self.hantar_children + self.hapash_children
        return sum(map(lambda cadet: cadet.state is not State.OMW, cadet_list))

    def get_summary(self) -> str:
        """
        Generates the vidutz's state summary in string format, to be left when the vidutz ends.
        :return: The summary.
        """
        template = 'סיכום וידו"צ\nנכחו: {num_here}\n{absentees}'
        cadet_list = sorted(self.hantar_children + self.hapash_children, key=VidutzData.key_func)
        num_here = sum(map(lambda cadet: cadet.state is State.HERE, cadet_list))
        absentee_list = [cadet.session.user.get_short_name() for cadet in cadet_list if cadet.state is not State.HERE]
        absentees_string = 'אין חסרים'
        if len(absentee_list) > 0:
            absentees_string = 'חסרים:\n{}'.format('\n'.join(absentee_list))
        return template.format(num_here=num_here, absentees=absentees_string)

    @staticmethod
    def key_func(vcd: VidutzCadetData) -> Tuple[State, str]:
        """
        Helper function - used as key function for sorting.
        :param vcd: A cadet
        :return: A tuple of (cadet's state, cadet's name)
        """
        return -vcd.state.value, vcd.session.user.get_short_name()
