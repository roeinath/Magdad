import os
import urllib.parse
from APIs.ExternalAPIs.FilesAPIs.talpix_file import TalpiXFile
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *


class DownloadButton(UIComponent):
    def __init__(self, text, file: TalpiXFile, bg_color="#2e7ea6", fg_color='none', size=SIZE_MEDIUM, font=None):
        super().__init__(text=text, bg_color=bg_color, fg_color=fg_color, size=size)
        self.__font = font
        if file is None:
            raise Exception("Cannot create a download button for no file")
        self.__filename = file.filename
        self.__filepath = file.path_on_server

    def render(self):
        return {
            JSON_TYPE: 'DownloadButton',
            JSON_ID: self.id,
            JSON_TEXT: self.text,
            JSON_ACTION: f'/get_file/?filepath={urllib.parse.quote(self.__filepath)}',
            JSON_SIZE: self.size,
            JSON_BG_COLOR: self.bg_color,
            JSON_FG_COLOR: self.fg_color,
            JSON_FONT: self.__font,
            JSON_FILE_PATH: os.path.split(self.__filepath)[1],
            JSON_FILE_NAME: self.__filename,
        }
