from web_framework.server_side.infastructure.category import Category
from web_framework.server_side.infastructure.constants import *
from web_features.talpiwiki import talpiwiki_main_page, view_shared
from web_features.talpiwiki import talpiwiki_tree_page
from APIs.TalpiotSystem import Vault


class TalpiWikiCategory(Category):
    def __init__(self):
        super().__init__(pages={
            'talpiwiki_main_page': talpiwiki_main_page.TalpiWikiMainPage,
            'talpiwiki_tree_page': talpiwiki_tree_page.TalpiWikiTreePage,
            'talpishared': view_shared.SharedPage
        })

    def get_title(self) -> str:
        return "שימור ידע"

    def is_authorized(self, user):
        return MATLAM in user.role  # Only the people of the base
