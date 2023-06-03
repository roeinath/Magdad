from web_features.tech_miun import permissions
from web_features.tech_miun.assessments.behavioral_diagnostician_miun_page import BehavioralDiagnosticianPage
from web_features.tech_miun.assessments.estimator_page import EstimatorPage
from web_features.tech_miun.handle_estimators import HandleEstimators
from web_features.tech_miun.master_page import MasterPage
from web_features.tech_miun.assessments.sagab_miun_page import SagabPage
from web_framework.server_side.infastructure.category import Category
from web_features.tech_miun_temp.wix.custom_page import CustomPage
from web_features.tech_miun_temp.report_creation.create_report_page import CreateReportPage
from web_features.tech_miun_temp.report_creation.create_wix import CreateWixPage
from web_features.tech_miun_temp.wix.wix_page import WixPage
from web_features.tech_miun_temp.estimator_evaluation.estimators_evaluation_page import EstimatorsEvaluationPage

# TODO: add documentation to class and methods
class MiunCategory(Category):
    def __init__(self):
        super().__init__(pages={
            "estimator_page": EstimatorPage,
            "saga_miun_page": SagabPage,
            "behavioral_diagnostician_miun_page": BehavioralDiagnosticianPage,
            "handle_estimators": HandleEstimators,
            "master_page": MasterPage,
            "custom_page": CustomPage,
            "create_report_page": CreateReportPage,
            "create_wix_page": CreateWixPage,
            "wix_page": WixPage,
            "estimators_evaluation_page": EstimatorsEvaluationPage,
        })

    def get_title(self) -> str:
        return "מיון והערכה"

    def is_authorized(self, user):
        return permissions.is_user_miun(user)
