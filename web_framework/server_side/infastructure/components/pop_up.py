from web_framework.server_side.infastructure import request_handlers, ids_manager
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *


class PopUp(UIComponent):

    def __init__(self, ui_component, is_shown, is_cancelable, title, close_action=None):
        super().__init__()
        self.__list = [ui_component]
        if isinstance(ui_component, UIComponent):
            self.add_component(ui_component)

        self.__is_shown = is_shown
        self.__is_cancelable = is_cancelable
        self.__title = title

        __close_action = close_action if close_action else lambda x: self.hide()

        func_id = ids_manager.gen_action_id(__close_action)
        self.__action = self.method_to_url(func_id)

    def render(self):
        return {
                JSON_TYPE: 'PopUp',
                JSON_ID: self.id,
                'is_shown': self.__is_shown,
                JSON_ACTION: self.__action,
                'is_cancelable': self.__is_cancelable,
                'title': self.__title
        }

    def add_component(self, ui_component, index=-1):
        if not isinstance(ui_component, UIComponent):
            return

        if index == -1:
            self.__list.append(ui_component)
        else:
            self.__list.insert(index, ui_component)

        self.add_action({
            JSON_ACTION: JSON_add_component,
            JSON_VALUE: {
                JSON_ID: self.id,
                JSON_CHILD: {
                    "component": ui_component.render()
                }
            }
        })

    def show(self):
        self.is_shown = True

        self.add_action({
            JSON_ACTION: 'change',
            JSON_VALUE: {
                JSON_ID: self.id,
                'is_shown': True
            }

        })

    def hide(self):
        self.is_shown = False

        self.add_action({
            JSON_ACTION: 'change',
            JSON_VALUE: {
                JSON_ID: self.id,
                'is_shown': False
            }
        })

    def get_first_level_children(self):
        return self.__list
