import web_features.tech_miun.constants as miun_const
from web_features.tech_miun import permissions
from web_features.tech_miun.assessments.assessments_page import AssessmentsPage


class SagabPage(AssessmentsPage):

    def __init__(self, params):
        super().__init__([], survey_list=miun_const.SURVEY_LIST_SAGAB)
        self.sp = None

    @staticmethod
    def get_title() -> str:
        return 'דף סג"ב'

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_sagab_miun(user)
