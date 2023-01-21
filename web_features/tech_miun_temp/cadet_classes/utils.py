import pandas as pd
import gdown as gd

from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.constants import *


def import_data_from_drive(url, save_path) -> None:
    """
    input: url - the folder in the drive witch the desired file is located
           save_path - the relative output path to save the file into (relative to "temp_files" folder)
    output: None
    """
    save_path = "./web_features/tech_miun_temp/temp_files/" + save_path
    gd.download(url, save_path, quiet=False, fuzzy=True)


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
