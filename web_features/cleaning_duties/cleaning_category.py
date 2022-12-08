from web_features.cleaning_duties.view_cleaning_points import ViewCleaningPoints
from web_features.cleaning_duties.view_cleaning_tasks import ViewCleaningTasks
from web_features.cleaning_duties.generate_cleaning_tasks import GenerateCleaningTasks
from web_features.cleaning_duties.cleaning_settings import CleaningSettings
from web_features.cleaning_duties.cleaning_history import CleaningHistory
from web_features.cleaning_duties.permissions import is_user_cleaning_task_admin
from web_framework.server_side.infastructure.category import Category
from web_framework.server_side.infastructure.constants import *


class CleaningCategory(Category):
    def __init__(self):
        super().__init__(pages={
            'cleaning_view': ViewCleaningTasks,
            'cleaning_generate': GenerateCleaningTasks,
            'cleaning_settings': CleaningSettings,
            'cleaning_points': ViewCleaningPoints,
            'cleaning_history': CleaningHistory
        })

    def get_title(self) -> str:
        return "תורנויות"

    def is_authorized(self, user):
        return MATLAM in user.role  # Only the people of the base
