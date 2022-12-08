from web_features.shagmach.classified_notebooks import ViewClassifiedNotebookStatus
from web_features.shagmach.view_blay import BlayRequests
from web_features.shagmach.view_computer_errors import ComputerErrors
from web_features.shagmach.building_errors import BuildingErrors
from web_features.shagmach.food_doc import FoodDoc
from web_features.shagmach.view_appointments import ViewDoctorAppointments
from web_features.shagmach.view_docs_to_fill import ViewDocsToFill
from web_framework.server_side.infastructure.category import Category
from web_framework.server_side.infastructure.constants import *


class ShagmachCategory(Category):
    def __init__(self):
        super().__init__(pages={
            'computer_errors': ComputerErrors,
            'blay_requests': BlayRequests,
            'building_errors': BuildingErrors,
            'food_doc': FoodDoc,
            'view_appointments': ViewDoctorAppointments,
            'view_docs_to_fill': ViewDocsToFill,
            'view_classified_notebook_status': ViewClassifiedNotebookStatus,
        })

    def get_title(self) -> str:
        return 'שגמ"ח'

    def is_authorized(self, user):
        return MATLAM in user.role  # Only the people of the base
