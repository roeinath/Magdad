from web_features.Elements.graph_page import graph_page
from web_framework.server_side.infastructure.category import Category
from web_framework.server_side.infastructure.constants import *
from web_features.Elements.personal_page.cadet_page import CadetPage
from web_features.Elements.personal_page.groups_page import GroupsPage
from web_features.Elements.personal_page.file_upload import FileUpload
from web_features.Elements.personal_page.forms_comparison import FormsComparison
from web_features.Elements.mental.mental_dashboard import MentalDashboardPage


class ElementsCategory(Category):
    def __init__(self):
        super().__init__(pages={
            "groups_page": GroupsPage,
            "cadets_page": CadetPage,
            "file_upload": FileUpload,
            "forms_comparison": FormsComparison,
            "mental_dashboard": MentalDashboardPage,
            "graph_page": graph_page,
        })

    def get_title(self):
        return "יסודות"

    def is_authorized(self, user):
        return MATLAM in user.role  # Only the people of the base
