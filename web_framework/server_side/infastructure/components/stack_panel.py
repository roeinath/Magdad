from web_framework.server_side.infastructure.ui_component import UIComponent
from typing import List
from web_framework.server_side.infastructure.constants import *
from typing import List

from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent

VERTICAL = 1
HORIZONTAL = 0


class StackPanel(UIComponent):
    def __init__(self, children: List[UIComponent] = [], orientation=VERTICAL):
        super().__init__()
        self.__list = []
        self.__orientation = orientation
        for comp in children:
            self.add_component(comp)

    def render(self):
        return {JSON_TYPE: 'StackPanel',
                JSON_ID: self.id,
                'orientation': self.__orientation
                }

    def add_component(self, ui_component, index=-1):
        ui_component.session_id = self.session_id
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

    def delete_component(self, comp):
        print("Deleting: " + str(comp) + " (" + str(type(comp)) + "). Is ui component: " + str(
            isinstance(comp, UIComponent)))
        if isinstance(comp, UIComponent):  # comp is a component, find its index and delete
            for i, curr in enumerate(self.__list):
                if comp == curr:
                    self.delete_component(i)
        else:  # Otherwise comp is a number, delete by index
            temp = self.__list[comp]
            del (self.__list[comp])
            self.add_action({
                JSON_ACTION: JSON_DELETE_CHILD,
                JSON_VALUE: {JSON_ID: self.id,
                             'component': temp.id,
                             }
            })

    def clear(self):
        indexes = list(range(len(self.__list)))
        indexes.reverse()

        for i in indexes:
            self.delete_component(i)

    def change_orientation(self):
        self.__orientation = not self.__orientation
        self.add_action({
            JSON_ACTION: 'change_orientation',
            JSON_VALUE: {JSON_ID: self.id,
                         }
        })

    def get_first_level_children(self):
        return self.__list
