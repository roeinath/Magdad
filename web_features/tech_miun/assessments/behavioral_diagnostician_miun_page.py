from web_features.tech_miun.assessments.assessments_page import AssessmentsPage
import web_features.tech_miun.constants as miun_const

from web_features.tech_miun import permissions


class BehavioralDiagnosticianPage(AssessmentsPage):

    def __init__(self, params):
        super().__init__([], survey_list=miun_const.SURVEY_LIST_BEHAVIOR_DIAGNOSTICIAN)
        self.sp = None

    @staticmethod
    def get_title() -> str:
        return "דף מאבחנת"

    @staticmethod
    def is_authorized(user) -> bool:
        return permissions.is_behavioral_diagnostician_miun(user)
