from typing import Dict

from APIs.TalpiotAPIs import NewForm
from web_features.Elements.mental.components.dashboard_card import DashboardCard
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.components.json_schema_newform import JsonSchemaNewForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.stack_panel import StackPanel


class AddDataCard(DashboardCard):
    def __init__(self, grid_start, grid_end, avlble_data: Dict, forms: Dict[str, NewForm]):
        super().__init__(grid_start, grid_end, 'הוספת נתונים')
        self._available_data = list(avlble_data.keys())
        self._forms = forms

        self._sp = StackPanel()

        self._selected_data_comp = ComboBox(avlble_data, self._set_selected_data)

        select_dat_sp = StackPanel(orientation='horizontal')
        select_dat_sp.add_component(Label('בחר נתון'))
        select_dat_sp.add_component(self._selected_data_comp)
        self._sp.add_component(select_dat_sp)

        if len(self._available_data) >= 1:
            self._selected_data = self._available_data[0]

            form = self._forms[self._selected_data]
            self._form = JsonSchemaNewForm(form, visible=['value', 'week', 'machzor'],
                                           submit=self._forms[self._selected_data].submit)
            self._sp.add_component(self._form)

        self.add_child(self._sp)

    def _update_form(self):
        try:
            self._sp.delete_component(1)
        except IndexError:
            pass

        form = self._forms[self._selected_data]
        self._form = JsonSchemaNewForm(form, visible=['value', 'week', 'machzor'],
                                       submit=self._forms[self._selected_data].submit)
        # self._sp.add_component(self._form)
        # self._form.change_form(form)

    def get_selected_data(self):
        return self._selected_data

    def _set_selected_data(self, data):
        if data in self._available_data:
            self._selected_data = data
            self._update_form()
            print(self._selected_data)
