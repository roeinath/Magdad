from typing import List

from mongoengine import *

from APIs.ExternalAPIs import GoogleDrive, FileToUpload
from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.TalpiShared.talpishared_object import TalpiSharedObject
from APIs.TalpiotAPIs.TalpiShared.talpishared_tags import TalpiSharedTag
from web_framework.server_side.infastructure import request_handlers
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.display_files import DisplayFile
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.hyper_link import HyperLink
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel, HORIZONTAL
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page

BUTTON_COLOR = "#F0F0F0"

BACKSLASH_URLENCODED = "%2F"
BASE_URL = '/react/page/talpishared'
FOLDER_URL = 'folder='
SEARCH_URL = 'search='


class SharedPage(Page):
    SHARED_DIR_ID = "1hdSM7SV4lv1HkpFghi-lC0eAOSO1kKzl"
    # Grid Panel for files
    GRID_COLUMNS = 6
    # Grid Panel for full page
    PAGE_GRID_COLUMNS = 6

    def __init__(self, params):
        super().__init__()
        self.gp: GridPanel = GridPanel(7, self.PAGE_GRID_COLUMNS, bordered=False)
        self.files_gp: GridPanel = GridPanel(100, self.GRID_COLUMNS, bordered=False)
        self.selected_tags: List[TalpiSharedTag] = []
        self.tags_search_sp = StackPanel([], orientation=HORIZONTAL)
        self.path: str = ''
        if len(params) > 0 and params[0] != 'undefined':
            self.path = params[0]
        self.google_drive = GoogleDrive().get_instance()
        self.search_tags_popup: PopUp = None
        self.title_label: Label = None
        self.current_dir: TalpiSharedObject = None

    @staticmethod
    def get_title() -> str:
        return "מבחני עבר"

    @staticmethod
    def is_authorized(user: User):
        return user.name in ["יותם אורן", "ליאור סימיונוביץ\'", "יהלי אקשטיין", "מדר תלפיות"]

    def get_page_ui(self, user: User):
        try:
            return self.draw_ui()
        except Exception as err:
            print("ERROR:", err.with_traceback(err.__traceback__))
            return DisplayFile(FileToUpload(name='מבחני עבר', file_type='folder',
                                            url=self.google_drive.get_folder_url_from_id(self.SHARED_DIR_ID)))

    def draw_ui(self):
        # self.update_mongo()
        self.title_label = Label(SharedPage.get_title(), size=SIZE_EXTRA_LARGE)
        # for i in range(self.gp.row_count):
        #     for j in range(self.gp.column_count):

        # padding for first part
        self.gp.add_component(Label(""), 0, 1, column_span=self.PAGE_GRID_COLUMNS // 3 - 1)
        # Title
        self.gp.add_component(self.title_label, 0, self.PAGE_GRID_COLUMNS // 3, column_span=self.PAGE_GRID_COLUMNS // 3)
        # Home
        self.gp.add_component(Button('🏠', action=lambda: self.redirect_to_uri(BASE_URL, True), bg_color=BUTTON_COLOR,
                                     size=SIZE_LARGE), 0, 0)
        # Edit
        self.gp.add_component(Button("✏️", action=None, bg_color=BUTTON_COLOR, size=SIZE_LARGE), 0,
                              self.PAGE_GRID_COLUMNS - 1)
        # Search
        self.gp.add_component(Button('🔎', action=self.set_search_form_tags_popup, bg_color=BUTTON_COLOR,
                                     size=SIZE_LARGE), 0, self.PAGE_GRID_COLUMNS - 2)

        self.gp.add_component(Label(""), 2, 0, column_span=self.PAGE_GRID_COLUMNS // 3)
        self.gp.add_component(Divider(), 2, self.PAGE_GRID_COLUMNS // 3, column_span=self.PAGE_GRID_COLUMNS // 3)

        self.gp.add_component(self.files_gp, 3, 0, column_span=self.PAGE_GRID_COLUMNS)
        self.current_dir = self.extract_base_dir_from_path()
        if self.current_dir:
            self.display_folder_content(self.current_dir)
            if self.current_dir.file_id:
                self.gp.add_component(
                    HyperLink("קישור לתיקייה בדרייב",
                              url=self.google_drive.get_folder_url_from_id(self.current_dir.file_id)),
                    4, 0, column_span=self.PAGE_GRID_COLUMNS
                )
        else:
            pass
            # self.gp.add_component(Label(f"התיקייה '{dir_name}' אינה קיימת. נסו לשנות את הurl ", fg_color='red'))
        return self.gp

    def extract_base_dir_from_path(self):
        if self.path:
            if self.path.startswith(FOLDER_URL):
                tags = self.path.replace(FOLDER_URL, '').split('/')
                return TalpiSharedObject.objects(tags=tags).first()
            if self.path.startswith(SEARCH_URL):
                path = self.path.replace(SEARCH_URL, '')
                name = path.replace('/', ', ')
                self.selected_tags = path.split('/')
                print("selected_tags", self.selected_tags)
                children = []
                # for tag in self.selected_tags:
                for talpishared_object in TalpiSharedObject.objects():
                    if all([tag in talpishared_object.tags for tag in self.selected_tags]):
                        children.append(talpishared_object)

                return TalpiSharedObject(name=name, tags=self.selected_tags, children=children)
        else:
            return TalpiSharedObject.objects(file_id=self.SHARED_DIR_ID).first()

    def update_mongo(self):
        for f in TalpiSharedObject.objects(file_id__ne=self.SHARED_DIR_ID):
            f.delete()
        base_dir = TalpiSharedObject.objects(file_id=self.SHARED_DIR_ID).first()
        base_dir.children = []
        base_dir.save()
        self.add_folder_to_mongo(base_dir)

    def display_folder_content(self, folder: TalpiSharedObject):
        def go_to_new_folder(folder_name):
            if not self.path:  # on the first folder chosen, add '/'
                self.redirect_to_uri(f'{BASE_URL}/{FOLDER_URL}{folder_name}', override=True)
            elif self.path.startswith(SEARCH_URL):
                talpishared_object = TalpiSharedObject.objects(name=folder_name).first()
                uri = BACKSLASH_URLENCODED.join(talpishared_object.tags)
                self.redirect_to_uri(f'{BASE_URL}/{FOLDER_URL}{uri}', override=True)
            else:
                print(self.path)
                self.redirect_to_uri(f'{BACKSLASH_URLENCODED}{folder_name}')

        self.files_gp.clear()
        self.files_gp.set_row_count(len(folder.children) // self.GRID_COLUMNS + 1)
        self.title_label.update_text(folder.name)

        for i, f in enumerate(folder.children):
            row = i // self.GRID_COLUMNS
            column = self.GRID_COLUMNS - i % self.GRID_COLUMNS - 1
            display_file_component = DisplayFile.from_talpishared_object(f)
            if f.children is not None:
                display_file_component.set_action(action=lambda ff=f: go_to_new_folder(ff.name))
            else:
                display_file_component.update_file_url(url=self.google_drive.get_url_from_id(f.file_id))
            self.files_gp.add_component(display_file_component, row, column)
        row = len(folder.children) // self.GRID_COLUMNS
        col = len(folder.children) % self.GRID_COLUMNS
        self.files_gp.add_component(Label(), row, 0, column_span=self.GRID_COLUMNS - col)

    def upload_file_to_mongo(self, file_id: str, name: str, tags: list, parent: TalpiSharedObject = None,
                             children: list = None) -> None:
        child = TalpiSharedObject.new_object(file_id, name, tags, children).save()
        parent.add_child(child)

    def add_folder_to_mongo(self, folder: TalpiSharedObject):
        # dirs = GoogleDrive.get_instance().list_files(self.SHARED_DIR_ID, False)
        for file_data in GoogleDrive.get_instance().list_files(folder.file_id, False)["files"]:
            f = FileToUpload.load_from_json(file_data)
            f_id = file_data['id']
            final = TalpiSharedObject.new_object(f_id, f.name, folder.tags + [f.name])
            if "folder" in file_data['mimeType'] or "shortcut" in file_data['mimeType']:
                final.children = []
                self.add_folder_to_mongo(final)
            final.save()
            folder.add_child(final, do_save=False)
        folder.save()

    def start_tag_search(self, tags_form):
        self.search_tags_popup.hide()
        uri = BACKSLASH_URLENCODED.join([t.tag for t in tags_form.tags])
        self.redirect_to_uri(f'{BASE_URL}/{SEARCH_URL}{uri}', override=True)

    def set_search_form_tags_popup(self):
        class TagSearchForm(Document):
            tags = ListField(ReferenceField(TalpiSharedTag))

        optional_tags = TalpiSharedTag.objects().order_by('priority')
        current_tags = [TalpiSharedTag.objects(tag=tag).first() for tag in self.selected_tags]
        form = JsonSchemaForm(TagSearchForm, visible=['tags'], display_name={'tags': 'תגיות'},
                              value=TagSearchForm(tags=current_tags),
                              options={'tags': optional_tags}, options_display={'tags': lambda x: x.tag},
                              submit=self.start_tag_search)
        self.search_tags_popup = PopUp(form, title="חיפוש", is_shown=True, is_cancelable=True)
        self.gp.add_component(self.search_tags_popup, 6, 0)

    def edit_current_folder(self):
        def edit_pop_up():
            pass
        (DisplayFile(self.files_gp.get_first_level_children()[0])).set_action(edit_pop_up)

    def redirect_to_uri(self, uri, override=False):
        request_handlers.actions_lsts[self.gp.session_id].append({
            JSON_ACTION: JSON_REDIRECT,
            JSON_VALUE: {
                JSON_ID: self.gp.id,
                JSON_URL: uri,
                'override': override
            }
        })

    # TODO:
    #  search bar
    #  add tags
    #  add file/s and create folder.
    #  delete file/folder
    #  change tags of folder/file
