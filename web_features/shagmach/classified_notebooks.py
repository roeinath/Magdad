from web_framework.server_side.infastructure.constants import *
from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.ClassifiedNotbooks.classified_notebooks import ClassifiedNotebook
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanel
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanelColumn
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page


class ViewClassifiedNotebookStatus(Page):
    @staticmethod
    def get_title() -> str:
        return "סטטוס מחברות ב\"מ"

    def __init__(self, params):
        super().__init__()
        self.sp = StackPanel([])

    def get_page_ui(self, user: User):
        self.sp.add_component(Label("סטטוס מחברות ב\"מ", size=SIZE_EXTRA_LARGE))

        notebooks = ClassifiedNotebook.objects()
        signed = 0
        locked = 0
        for notebook in notebooks:
            if notebook.is_locked:
                locked += 1
            else:
                signed += 1
        self.sp.add_component(Label(f"כמות מחברות: {len(notebooks)}"))
        self.sp.add_component(Label(f"מחברות משוכות: {signed}"))
        self.sp.add_component(Label(f"מחברות נעולות: {locked}"))

        self.sp.add_component(DocumentGridPanel(ClassifiedNotebook, column_list=[
            DocumentGridPanelColumn('user', "בעל/ת המחברת", lambda _, user: Label(user.name)),
            DocumentGridPanelColumn('is_locked', "האם נעולה",
                                    lambda _, is_locked: Label("כן" if is_locked else "לא",
                                                               fg_color='black' if is_locked else 'red')),
        ], order_by=['is_locked']))

        return self.sp
