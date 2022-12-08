from web_features.guardings.guarding_history import GuardingHistory
from web_features.guardings.view_points import ViewPoints
from web_features.guardings import generate_guardings, guarding_settings
from web_features.guardings import view_guardings
from web_features.guardings import view_points
from web_framework.server_side.infastructure.category import Category
from web_framework.server_side.infastructure.constants import *


class GuardingCategory(Category):
    def __init__(self):
        super().__init__(pages={
            'guarding_view': view_guardings.ViewGuardings,
            'guarding_generate': generate_guardings.GenerateGuardings,
            'guarding_settings': guarding_settings.GuardingSettings,
            'guarding_points': view_points.ViewPoints,
            'guarding_history': GuardingHistory
        })

    def get_title(self) -> str:
        return "שמירות"

    def is_authorized(self, user):
        return MATLAM in user.role  # Only the people of the base
