from web_features.talpix.documentation.documentation_components import get_page_by_file
from web_framework.server_side.infastructure.page import Page


class BaseDocumentationPage(Page):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    def get_page_ui(self, user):
        return get_page_by_file(self.file_name)


class IntroDev(BaseDocumentationPage):
    def __init__(self):
        super().__init__('intro_dev.txt')

    @staticmethod
    def get_title():
        return "תחילת פיתוח"


class ComponentsDescription(BaseDocumentationPage):
    def __init__(self):
        super().__init__('components_description.txt')

    @staticmethod
    def get_title():
        return "תיאור קומפוננטים"

