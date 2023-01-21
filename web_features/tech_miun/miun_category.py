from web_features.tech_miun import permissions
from web_features.tech_miun.assessments.behavioral_diagnostician_miun_page import BehavioralDiagnosticianPage
from web_features.tech_miun.assessments.estimator_page import EstimatorPage
from web_features.tech_miun.handle_estimators import HandleEstimators
from web_features.tech_miun.master_page import MasterPage
from web_features.tech_miun.assessments.sagab_miun_page import SagabPage
from web_features.tech_miun_temp.assessments.zoer_page import ZoerPage
from web_features.tech_miun_temp.assessments.zoer_dummy_page import DummyZoerPage
from web_features.tech_miun_temp.assessments.drive_test_page import DriveTestPage
from web_framework.server_side.infastructure.category import Category


# TODO: add documentation to class and methods
class MiunCategory(Category):
    def __init__(self):
        super().__init__(pages={
            "estimator_page": EstimatorPage,
            "saga_miun_page": SagabPage,
            "behavioral_diagnostician_miun_page": BehavioralDiagnosticianPage,
            "handle_estimators": HandleEstimators,
            "master_page": MasterPage,
            "zoer_page": ZoerPage,
            "dummy_zoer_page": DummyZoerPage,
            "drive_test_page": DriveTestPage
        })

    def get_title(self) -> str:
        return "מיון והערכה"

    def is_authorized(self, user):
        return permissions.is_user_miun(user)
