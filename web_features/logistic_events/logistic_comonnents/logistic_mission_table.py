from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.LogisticEvents.logistic_event import LogisticEvent
from APIs.TalpiotAPIs.LogisticEvents.logistic_event_missions import LogisticEventMission
from web_features.logistic_events.logistic_comonnents.general_logistic_components import GeneralLogisticComponents
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanelColumn, \
    DocumentGridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel


class LogisticMissionTable(GeneralLogisticComponents):

    def get_missions_table(self, logistic_event: LogisticEvent):
        column_list = [
            DocumentGridPanelColumn('approved', " ", component_parser=self.approve_status_component),
            DocumentGridPanelColumn('description', "משימה"),
            DocumentGridPanelColumn('users_in_charge', "מי מבצע/ת", component_parser=lambda status, users:
            self.users_list_names(status, field='users_in_charge')),
            DocumentGridPanelColumn('deadline', "דדליין", component_parser=self.deadline_component),
            DocumentGridPanelColumn('comments', "הערות", component_parser=self.status_comments_component),
        ]
        if self.is_user_logistic_permitted(logistic_event):
            column_list.append(
                DocumentGridPanelColumn('logistic_event', ' ', component_parser=self.delete_object_component)
            )
        table = DocumentGridPanel(
            LogisticEventMission, column_list=column_list,
            filter_by={'logistic_event': logistic_event}, order_by=['approved', 'deadline'],
        )
        table.update_color()
        return table

    def get_missions_buttons(self, logistic_event: LogisticEvent):
        buttons = StackPanel([])
        if self.is_user_logistic_permitted(logistic_event):
            buttons.add_component(Button("הוספת משימה ➕", lambda event=logistic_event: self.add_mission_form(event)))
        return buttons

    ############
    # MISSIONS #
    ############
    def add_mission_form(self, logistic_event: LogisticEvent):
        def add_mission(new_mission: LogisticEventMission):
            new_mission.logistic_event = logistic_event
            new_mission.save()
            self.logistic_page.popup.hide()
            self.draw_tables()

        default_value = LogisticEventMission.new_mission(logistic_event, description='', comments='')
        form = JsonSchemaForm(
            LogisticEventMission,
            value=default_value,
            visible=['description', 'users_in_charge', 'deadline', 'comments'],
            display_name={'description': 'משימה', 'deadline': 'דד ליין', 'comments': 'הערות',
                          'users_in_charge': 'אחראיים'},
            options={'users_in_charge': User.objects},
            options_display={'users_in_charge': lambda x: x.get_full_name()},
            paragraphTexts=['comments'],
            submit=add_mission
        )

        self.logistic_page.popup = PopUp(form, title="הוספת משימה", is_shown=True, is_cancelable=True)
        self.logistic_page.sp.add_component(self.logistic_page.popup)
