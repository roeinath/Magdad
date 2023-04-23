from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure import ids_manager

PYTHON = 'python'
DRACULA = 'dracula'


class RichTextEditor(UIComponent):
    def __init__(self, html: str = "", width="70vw", height="40vh"):
        super().__init__()
        self.__html = html
        self.__width = width
        self.__height = height

        func_id = ids_manager.gen_action_id(self.__update_html)
        self.__action = self.submit_to_url(func_id)

    def render(self):
        return {
            JSON_TYPE: 'RichTextEditor',
            JSON_ID: self.id,
            JSON_INITIAL_STATE: self.__html,
            JSON_WIDTH: self.__width,
            JSON_HEIGHT: self.__height,
            JSON_ACTION: self.__action
        }

    def __update_html(self, html):
        self.__html = html

    def update_html(self, html):
        self.__update_html(html)
        self.add_action({
            JSON_ACTION: JSON_CHANGE,
            JSON_VALUE: {
                JSON_ID: self.id,
                JSON_INITIAL_STATE: self.__html
            }
        })

    def get_code(self):
        return self.text
