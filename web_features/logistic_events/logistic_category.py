from web_features.logistic_events.manage_logistic_statuses import ManageLogisticStatuses
from web_features.logistic_events.view_docs import ViewDocs
from web_features.logistic_events.view_logistic_events import ViewLogisticEvents
from web_framework.server_side.infastructure.category import Category
from web_framework.server_side.infastructure.constants import *


class LogisticEventsCategory(Category):
    def __init__(self):
        super().__init__(pages={
            'events': ViewLogisticEvents,
            'docs': ViewDocs,
            'manage_logistic_statuses': ManageLogisticStatuses
        })

    def get_title(self) -> str:
        return "אירועים"

    def is_authorized(self, user):
        return MATLAM in user.role  # Only the people of the base
