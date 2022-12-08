from typing import Optional

from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.Telegram.View.telegram_button_group_view import TelegramButtonGroupView
from bot_framework.View.button_group_view import ButtonGroupView
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.ui import UI, Button
from bot_features.Mahzori.Vidutz.Code.state import State
from bot_features.Mahzori.Vidutz.Code.vidutz_cadet_data import VidutzCadetData
from bot_features.Mahzori.Vidutz.Code.vidutz_data import VidutzData
from APIs.TalpiotAPIs.Constraint.UserConstraint.user_constraint import UserConstraint, MachzorConstraint
from APIs.TalpiotAPIs.User.user import User
from bot_features.SystemFeatures.HierarchicalMenu.Code.hierarchical_menu import HierarchicalMenu


# todo debug this feature
class Vidutz(BotFeature):

    def __init__(self, ui: UI):
        """
        Create a new vidutz module instance
        :param ui: UI instance to be used
        """
        super().__init__(ui)

    def main(self, session: Session) -> None:
        """
        Called when the /vidutz command is received. Initialized a VidutzData and send vidutz messages.
        :param session: The caller's session object
        """
        def return_to_menu(session: Session):
            self.ui.clear(session)
            HierarchicalMenu.run_menu(self.ui, session.user)

        self.ui.create_button_group_view(session, "הפיצ'ר עבר דירה 🏠\n"
                                                  "כדי לבצע וידוא צוערים אנא כנסו ל:\n"
                                                  "תכניתי ⬅️ וידוא צוערים ⬅️ שם הקבוצה שאותה תרצו לבדוק",
                                         [Button("🔙", lambda s: (return_to_menu(s)))]).draw()

        # # This method is no longer relevant
        # users = UserConstraint.get_users_with_constraint(MachzorConstraint(session.user.mahzor))
        # session.data = VidutzData(session, self.ui)
        # for user in users:
        #     user_session = self.ui.create_session('vidutz', user)
        #     if user == session.user:  # don't create another session for initiating hantar
        #         pass
        #     elif "חנתר" in user_session.user.role:
        #         session.data.add_hantar(user_session)
        #         user_session.data = session.data
        #     else:
        #         session.data.add_hapash(user_session)
        #         user_session.data = session.data
        # session.data.sort()
        # self.initialize_views(session.data)

    def update_cadet(self, vidutz: VidutzData, cadet: VidutzCadetData, state: State):
        """
        Updates a single cadet's state and updates views accordingly.
        :param vidutz: The relevant vidutz
        :param cadet: The Cadet to be updated (must be in given vidutz)
        :param state: The cadet's new state
        """
        cadet.state = state
        self.update_views(vidutz, cadet)

    def initialize_views(self, vidutz: VidutzData):
        """
        Sends vidutz messages to all cadets in given vidutz
        :param vidutz: An initialized vidutz object
        """
        for cadet in vidutz.all_children:
            self.ui.create_button_group_view(cadet.session, 'מתחיל וידו"צ...', buttons=list()).draw()
        self.update_views(vidutz, to_all=True)
        # cadet_callback = lambda cadet, state: self.update_cadet(vidutz, cadet, state)
        # for hantar in vidutz.hantar_children:
        #     self.ui.create_button_group_view(hantar.session, r'וידו"צ בתהליך...',
        #                                      vidutz.get_buttons(cadet_callback, hantar,
        #                                                         close_callback=lambda test: self.finish_vidutz(vidutz),
        #                                                         sort_callback=lambda test: self.update_views(vidutz),
        #                                                         hantar=True)).draw()
        # for hapash in vidutz.hapash_children:
        #     self.ui.create_button_group_view(hapash.session, r'וידו"צ צוותי',
        #                                      vidutz.get_buttons(cadet_callback, cadet=hapash)).draw()

    def update_views(self, vidutz: VidutzData, updated_cadet: Optional[VidutzCadetData] = None, to_all: bool = False):
        """
        Updates views for all hantars as well as (optionally) given hapash an their teammates.
        :param vidutz: The relevant vidutz object
        :param updated_cadet: The cadet who's change triggered the update
        :param to_all: Will update all cadets' views if True
        """

        def cadet_callback(cadet: VidutzCadetData, state: State) -> None:
            return self.update_cadet(vidutz, cadet, state)

        for hantar in vidutz.hantar_children:
            view = hantar.session.view_container.views[0]

            if isinstance(view, TelegramButtonGroupView):
                view.update(new_text=r'וידו"צ בתהליך...', new_buttons=vidutz.get_buttons(
                    cadet_callback, hantar, close_callback=lambda test: self.finish_vidutz(vidutz),
                    sort_callback=lambda test: self.update_views(vidutz), hantar=True))

        if updated_cadet is not None or to_all:
            # get cadet's teammates' VidutzCadetData
            all_list = [cadet for cadet in vidutz.hantar_children + vidutz.hapash_children if
                        cadet not in vidutz.hantar_children]
            all_list.sort(key=VidutzData.key_func)

            if not to_all:
                user_list = updated_cadet.session.user.get_team()
                all_list = [cadet for cadet in all_list if (cadet.session.user in user_list)]

            for hapash in all_list:
                view: ButtonGroupView = hapash.session.view_container.views[0]

                if isinstance(view, TelegramButtonGroupView):
                    view.update(new_text=r'וידו"צ צוותי', new_buttons=vidutz.get_buttons(cadet_callback,
                                                                                         cadet=hapash))

    def finish_vidutz(self, vidutz: VidutzData):
        """
        Clear vidutz views and send summary messages to the hantars
        :param vidutz: The vidutz to be closed
        """
        for hapash in vidutz.hapash_children:
            self.ui.summarize_and_close(hapash.session, list())
        hantar_summary = vidutz.get_summary()
        for hantar in vidutz.hantar_children:
            self.ui.summarize_and_close(hantar.session, [self.ui.create_text_view(hantar.session, hantar_summary)])

    def get_summarize_views(self, session: Session) -> [View]:
        return list()

    def is_authorized(self, user: User) -> bool:
        return "חנתר" in user.role

    def get_command(self) -> str:
        return "vidutz"

    def get_scheduled_jobs(self):
        return list()
