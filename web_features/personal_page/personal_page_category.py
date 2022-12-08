from web_framework.server_side.infastructure.category import Category
from web_framework.server_side.infastructure.constants import *
from web_features.personal_page.cadet_page import CadetPage
from web_features.personal_page.groups_page import GroupsPage
from web_features.personal_page.file_upload import FileUpload
from web_features.personal_page.forms_comparison import FormsComparison


class PersonalPageCategory(Category):
    def __init__(self):
        super().__init__(pages={
            "groups_page": GroupsPage,
            "cadets_page": CadetPage,
            "file_upload": FileUpload,
            "forms_comparison.": FormsComparison
        })

    def get_title(self):
        return "יסודות"

    def is_authorized(self, user):
        return MATLAM in user.role  # Only the people of the base
