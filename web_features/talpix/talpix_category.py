from web_features.talpix.bot_signup import BotSignup
from web_features.talpix.documentation.documentation_pages import IntroDev, ComponentsDescription
from web_features.talpix.first_mvp import FIRST_MVP
from web_features.talpix.features_suggestions import FeaturesSuggestions
from web_features.talpix.ide_demo import IDEDemo, IDE_DEMO_PAGE_URI
from web_features.talpix.ide import IDE, IDE_PAGE_URI
from web_features.talpix.talpiot_users import TalpiotUsers
from web_features.talpix.talpix_logs import TalpiXLogs
from web_features.talpix.documentation.bot_wiki import BotWiki
from web_framework.server_side.infastructure.category import Category
from web_framework.server_side.infastructure.constants import *
from web_features.talpix.files_management import FilesManager


class TalpiXCategory(Category):
    def __init__(self):
        super().__init__(pages={
            'talpibot_users': TalpiotUsers,
            "intro_dev": IntroDev,
            "components_description": ComponentsDescription,
            "bot_wiki": BotWiki,
            'suggestions': FeaturesSuggestions,
            "bot_signup": BotSignup,
            'general_test': FIRST_MVP,
            IDE_DEMO_PAGE_URI: IDEDemo,
            IDE_PAGE_URI: IDE,
            'logs': TalpiXLogs,
            'files': FilesManager
        })

    def get_title(self) -> str:
        return "TalpiX"

    def is_authorized(self, user):
        return MATLAM in user.role  # Only the people of the base
