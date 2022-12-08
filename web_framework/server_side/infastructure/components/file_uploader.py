import os
from pathlib import Path
from typing import Callable, Any, List
from APIs.TalpiotAPIs.User.user import User
from web_features import talpix

import web_framework.server_side.infastructure.ids_manager as ids_manager
from APIs.ExternalAPIs import FileToUpload
from APIs.ExternalAPIs.FilesAPIs.files_api import upload_file
from APIs.ExternalAPIs.FilesAPIs.talpix_file import TalpiXFile
import APIs.ExternalAPIs.FilesAPIs as FilesAPIsDirectory
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.display_files import DisplayFile
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.ui_component import UIComponent

TEMP_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(FilesAPIsDirectory.__file__)), 'temp_files')


class DragUploader(UIComponent):
    def __init__(self, update_files: Callable = None):
        super().__init__()
        self.__sp = StackPanel([])
        if update_files:
            func_id = ids_manager.gen_action_id(update_files)
            self.__action = self.method_to_url(func_id)
        else:
            self.__action = None

    def render(self):
        return {
            JSON_TYPE: JSON_UPLOAD,
            JSON_ACTION: self.__action,
            JSON_ID: self.id
        }


class FileUploader(UIComponent):
    def __init__(self, on_file_uploaded: Callable[[TalpiXFile], Any] = None, upload_owner: User = None):
        super().__init__()

        if upload_owner is None:
            raise Exception("upload owner cannot be None")
        self.__upload_owner = upload_owner

        self.__sp = StackPanel([])
        self.__initiate_sp()

        self.__files: List[FileToUpload] = []
        self.__on_file_uploaded = on_file_uploaded

    def __update_files(self, data):
        print(data)
        self.__files = [FileToUpload.load_from_json(f) for f in data.get('files', [])]
        self.__sp.delete_component(self.__drag_uploader)
        for file_to_upload in self.__files:
            self.__display_file_sp.add_component(DisplayFile(file_to_upload))
        self.__button_sp.add_component(Button("העלאה", action=self.__on_upload_button_press))
        self.__button_sp.add_component(Button("ביטול", action=self.__initiate_sp, bg_color='red'))

    def __initiate_sp(self):
        self.__files: List[TalpiXFile] = []

        self.__sp.clear()
        self.__drag_uploader = DragUploader(self.__update_files)
        self.__display_file_sp = StackPanel([], orientation=HORIZONTAL)
        self.__button_sp = StackPanel([], orientation=HORIZONTAL)
        for comp in [self.__drag_uploader, self.__display_file_sp, self.__button_sp]:
            self.__sp.add_component(comp)

    def __on_upload_button_press(self):
        for file_to_upload in self.__files:
            Path(TEMP_FILE_DIR).mkdir(parents=True, exist_ok=True)
            temp_file_path = os.path.join(TEMP_FILE_DIR, file_to_upload.name)

            with open(temp_file_path, 'wb+') as temp_file:
                temp_file.write(file_to_upload.get_content())
            talpix_file = upload_file(temp_file_path)
            talpix_file.owner = self.__upload_owner
            talpix_file.shared_with = []
            talpix_file.save()
            os.remove(temp_file_path)

            print(talpix_file.filename, talpix_file.path_on_server)
            if self.__on_file_uploaded is not None:
                self.__on_file_uploaded(talpix_file)
        self.__initiate_sp()

    def render(self):
        return self.__sp.render()
