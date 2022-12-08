from web_framework.server_side.infastructure.category import Category
from web_framework.server_side.infastructure.constants import *
from web_features.IDE import view_IDE_development


class IDECategory(Category):
    def __init__(self):
        super().__init__(pages={
            'view_ide_category': view_IDE_development.ViewIDE,
        })

    def get_title(self) -> str:
        return "פיתוח"
