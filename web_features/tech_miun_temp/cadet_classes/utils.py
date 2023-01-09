import pandas as pd

from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.constants import *

SIZE_EXTRA_SMALL = 'xs'
SIZE_SMALL = 'sm'
SIZE_MEDIUM = 'md'
SIZE_LARGE = 'lg'
SIZE_EXTRA_LARGE = 'xl'


def data_frame_to_grid_panel(df: pd.DataFrame):
    """
    :param df: the data frame
    :return: a grid panel with the data frame as components
    """
    gp = GridPanel(len(df.to_numpy()) + 4, len(df.columns))

    for i, title in enumerate(df.columns):
        gp.add_component(Label(title, size=SIZE_LARGE, fg_color="white"), row=0, column=i,
                         bg_color=COLOR_PRIMARY_DARK)
        for j, data in enumerate(df.to_numpy()[:, i]):
            if not data:
                gp.add_component(Label(text="לא ידוע"), row=j + 1, column=i)
            else:
                gp.add_component(Label(text=str(data)), row=j + 1, column=i)

    return gp


class Data:
    def __init__(self, title, value, is_semesterial=False, is_open=False):
        self.value = value
        self.title = title
        self.is_semesterial = is_semesterial
        self.is_open = is_open
