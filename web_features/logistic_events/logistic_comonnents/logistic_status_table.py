from APIs.TalpiotAPIs.LogisticEvents.logistic_event import LogisticEvent
from web_features.logistic_events.logistic_comonnents.general_logistic_components import GeneralLogisticComponents
from web_framework.server_side.infastructure.components.confirmation_button import ConfirmationButton
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanelColumn
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.constants import *


class LogisticStatusTable(GeneralLogisticComponents):

    def get_status_table_colors(self, logistic_event_statuses):
        row_colors = {0: (COLOR_PRIMARY_DARK, 'white')}
        current_status_colored = False
        for i, status in enumerate(logistic_event_statuses, start=1):
            if not status.approved and not current_status_colored:
                row_colors[i] = COLOR_LIGHT_BLUE, COLOR_BLACK
                current_status_colored = True
            if not status.relevant:
                row_colors[i] = COLOR_GRAY, COLOR_BLACK
        return row_colors

    def get_status_table(self, logistic_event: LogisticEvent):
        column_list = [
            DocumentGridPanelColumn('approved', " ", component_parser=self.approve_status_component),
            DocumentGridPanelColumn('status_name', "שם"),
            DocumentGridPanelColumn('permitted_users', "מי מאשר/ת", component_parser=lambda st, users, event:
            self.users_list_names(st, field='permitted_users')),
            DocumentGridPanelColumn('deadline', "דדליין", component_parser=self.deadline_component),
            DocumentGridPanelColumn('attached_file_link', "מסמך מצורף",
                                    component_parser=self.attached_file_component),
            DocumentGridPanelColumn('comments', "הערות", component_parser=self.status_comments_component),
        ]
        if self.is_user_logistic_permitted(logistic_event):
            column_list.append(
                DocumentGridPanelColumn('approved', ' ', component_parser=self.delete_status_component)
            )

        logistic_event_statuses = logistic_event.statuses
        row_colors = self.get_status_table_colors(logistic_event_statuses)

        table = GridPanel(row_count=len(logistic_event.statuses) + 1, column_count=len(column_list))

        for j, column in enumerate(column_list):
            bg_color, fg_color = row_colors[0]
            table.add_component(Label(column.title, fg_color=fg_color), row=0, column=j, bg_color=bg_color)

        for i, status in enumerate(logistic_event_statuses, start=1):
            for j, column in enumerate(column_list):
                field_attr = getattr(status, column.field)
                component = column.component_parser(status, field_attr, logistic_event)
                if not component:
                    continue
                bg_color, _ = row_colors.get(i, (COLOR_TRANSPARENT, COLOR_BLACK))
                table.add_component(component, row=i, column=j, bg_color=bg_color)

        return table

    def delete_status_component(self, status, _, logistic_event: LogisticEvent = None):
        def delete_status():
            if status in logistic_event.statuses:
                logistic_event.statuses.remove(status)
                logistic_event.save()
            self.external_google_manager.delete_status_from_calendar(status)
            self.delete_object_and_refresh(status)

        if self.is_user_logistic_permitted(status):
            return ConfirmationButton("מחיקה", action=delete_status, bg_color=COLOR_RED)
        return Label("")
