from APIs.TalpiotAPIs import *
from APIs.TalpiotAPIs.static_fields import update_db_collections
from APIs.TalpiotSystem import Vault
from bot_features.SystemFeatures.HierarchicalMenu.Code.hierarchical_menu import HierarchicalMenu
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.button import Button
from bot_framework.ui.ui import UI


class DBCollectionsUpdate(BotFeature):


    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)

    def main(self, session: Session):
        self.ui.clear(session)
        buttons = [
            Button("שמור תיעוד של הcollections נוכחיים", lambda s: update_db_collections()),
            Button("עדכן את הDB", self.open_update_dialog),
            Button("🔙", self.return_to_menu)
        ]
        self.ui.create_button_group_view(session, "מה ברצונך לעשות?", buttons).draw()

    def open_update_dialog(self, session: Session):
        self.ui.create_text_view(session, "איזה DB תרצה לעדכן?").draw()
        self.ui.get_text(session, self.update_and_sync_db_collections)

    def update_and_sync_db_collections(self, session: Session, db_name):
        self.ui.create_text_view(session, "עלול לקחת רגע...").draw()
        collections = update_db_collections()
        synced_collections = Vault.get_vault().sync_db_to_main(collections, db_name, wait_until_finished=True)
        text = "```עודכנו:\n"
        for collection_name in sorted(synced_collections):
            text += f"{collection_name}: {synced_collections[collection_name]} new documents\n"
        text += "```"
        self.ui.clear(session)
        self.ui.create_text_view(session, text).draw()

    def get_summarize_views(self, session: Session) -> [View]:
        pass

    def is_authorized(self, user: User) -> bool:
        return user.bot_admin

    def scheduled_jobs_parser(self):
        update_db_collections()
        self.schedule_job(datetime.datetime.now() + datetime.timedelta(hours=3))

    def return_to_menu(self, session: Session):
        HierarchicalMenu.run_menu(self.ui, session.user)
