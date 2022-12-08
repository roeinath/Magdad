from web_features.cleaning_duties.view_cleaning_tasks import ViewCleaningTasks
from web_features.guardings.view_guardings import ViewGuardings
from web_features.logistic_events.view_logistic_events import ViewLogisticEvents
from web_features.shagmach.building_errors import BuildingErrors
from web_features.shagmach.view_blay import BlayRequests
from web_features.shagmach.view_computer_errors import ComputerErrors


def quick_access_page_list():
    return [
        ViewGuardings,
        ViewCleaningTasks,
        ComputerErrors,
        BlayRequests,
        BuildingErrors,
        ViewLogisticEvents,
    ]
