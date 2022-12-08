from APIs.TalpiotAPIs.TVS.tv_image_link import TVImageLink
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.constants import *


class AddImage(Page):
    @staticmethod
    def get_title() -> str:
        return "הוספת תמונה לטלוויזיה מחזורית"

    def create_request(self):
        def save_request(x: TVImageLink):
            x.mahzor = self.user.mahzor
            x.save()
            self.draw()

        form = JsonSchemaForm(TVImageLink, visible=['url', 'greeting'],
                              display_name={
                                  'url': 'קישור לתמונה להציג',
                                  "greeting": 'כיתוב להוספה על התמונה',
                              },
                              placeholder={
                                  "url": 'לדוגמה: http://example.jpeg',
                                  'greeting': 'כיתוב על התמונה',
                              },
                              submit=save_request)

        self.popup = PopUp(form, title="הוספת התמונה", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def __init__(self, params):
        super().__init__()
        self.container_table = None
        self.popup = None

        self.is_edit_possible = False
        self.is_screenshot_mode = False

        self.user = None

    def draw(self):
        self.sp.clear()

        self.sp.add_component(Label("הוספת תמונה לטלוויזיה המחזורית", size=SIZE_EXTRA_LARGE))
        buttons_panel = StackPanel([], orientation=0)
        self.sp.add_component(buttons_panel)
        self.sp.add_component(Label())

        buttons_panel.add_component(Button("הוסף תמונה לטלוויזיה", self.create_request))

    def get_page_ui(self, user):
        self.user = user
        self.sp = StackPanel([])
        self.draw()
        return self.sp
