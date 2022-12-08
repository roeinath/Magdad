from abc import ABC

from web_framework.server_side.infastructure.components.hyper_link import HyperLink
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.upload_files import UploadFiles
from web_framework.server_side.infastructure.components.display_files import DisplayFile
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.pop_up import PopUp


from APIs.TalpiotAPIs import BaseWikiPage
from APIs.ExternalAPIs import FileToUpload
from APIs.ExternalAPIs.GoogleDrive.google_drive import GoogleDrive
from APIs.TalpiotAPIs import TagList

import web_features.talpiwiki.constants as constants
import web_features.talpiwiki.util as util


class WikiBlock(StackPanel):
    # block_title - string with the block title
    # block_content - string / list with the content
    # block_styling - dictionary with styling instructions
    #   disp_title - bool

    DEFAULT_TITLE = "כותרת בלוק"
    DEFAULT_CONTENT = "בלוק"
    DEFAULT_STYLING = {
        "disp_title": True,
        "collapsible": False
    }

    def __init__(self, block_content=None, block_title=None, block_styling=None):
        super().__init__([])

        if block_styling is None:
            block_styling = WikiBlock.DEFAULT_STYLING

        if block_content is None:
            block_content = WikiBlock.DEFAULT_CONTENT

        if block_title is None:
            block_title = WikiBlock.DEFAULT_TITLE

        self.block_content = block_content
        self.block_title = block_title
        self.block_styling = block_styling

    def render(self):
        if self.block_styling.get('collapsible', False):
            self.block_styling['collapsible'] = False
            self.block_styling['disp_title'] = False
            self.block_styling['fill_to_max_row'] = False
            self.delete_component(self.get_first_level_children()[0])

            return Accordion([self], [self.block_title]).render()
        return super(WikiBlock, self).render()

    def add_title(self):
        self.title_label = Label(self.block_title, size='md', bold=True)
        if self.block_styling["disp_title"]:
            self.add_component(self.title_label)


class WikiHeader(WikiBlock):
    DEFAULT_STYLING = {
        "size": "xl",
        "bold": False
    }

    def __init__(self, block_content, block_title=None, block_styling=None):
        if block_styling is None:
            block_styling = WikiHeader.DEFAULT_STYLING

        block_styling = {**WikiHeader.DEFAULT_STYLING, **block_styling}

        super().__init__(block_content=block_content, block_title=block_title, block_styling=block_styling)
        self.add_component(Label(self.block_content, size=block_styling["size"], bold=block_styling["bold"]))


class WikiDivider(WikiBlock):
    BLOCK_STYLING = {
        "long": False,
        "disp_title": False
    }

    def __init__(self, block_content=None, block_title=None, block_styling=None):
        if block_styling is None:
            block_styling = WikiDivider.BLOCK_STYLING

        block_styling = {**WikiDivider.BLOCK_STYLING, **block_styling}

        super().__init__(block_content=block_content, block_title=block_title, block_styling=block_styling)

        if self.block_styling["long"]:
            self.add_component(WikiGrid(
                block_content=[[]],
                block_styling={"disp_title": False},
            ))
        else:
            self.add_component(Divider())


class WikiOneLiner(WikiBlock):
    def __init__(self, block_content, block_title=None, block_styling=None):
        super().__init__(block_content=block_content, block_title=block_title, block_styling=block_styling)

        if type(self.block_content) == list:
            self.block_content = ", ".join(self.block_content)

        if not self.block_styling["disp_title"]:
            disp_str = self.block_content
        else:
            disp_str = f"{self.block_title}: {self.block_content}"

        self.add_component(Label(disp_str, size='md'))


class WikiParagraph(WikiBlock):
    def __init__(self, block_content, block_title=None, block_styling=None):
        super().__init__(block_content=block_content, block_title=block_title, block_styling=block_styling)

        if self.block_content == "":
            return

        self.add_title()

        bg_color = None
        if 'bg_map' in self.block_styling:
            bg_color = self.block_styling['bg_map'].get(self.block_content, None)

        if type(self.block_content) == list:
            self.block_content = ", ".join(self.block_content)

        self.add_component(Label(self.block_content, size='md', bg_color=bg_color))


class WikiGrid(WikiBlock):
    DEFAULT_CONTENT = [[]]
    DEFAULT_STYLING = {
        "disp_title": True,
        "bold_first_row": False,
        "max_row_size": 5,
        "disp_empty": False,
        "fill_to_max_row": True,
        "last_val_sep_row": False,
        "bordered": True
    }

    def __init__(self, block_content=None, block_title=None, block_styling=None):
        if block_styling is None:
            block_styling = WikiGrid.DEFAULT_STYLING
        if block_content is None:
            block_content = WikiGrid.DEFAULT_CONTENT

        # Merge unspecified deafults
        block_styling = {**WikiGrid.DEFAULT_STYLING, **block_styling}

        super().__init__(block_content=block_content, block_title=block_title, block_styling=block_styling)

        # check for valid grid
        grid = self.block_content

        if len(grid) == 0 and not self.block_styling["disp_empty"]:
            return

        self.add_title()

        # make everything 2D
        if type(grid[0]) != list:
            grid = [grid]

        # handle rows that are too big:
        if self.block_styling["last_val_sep_row"]:
            last_val = grid[-1][-1]
            grid[-1] = grid[-1][:-1]
            padding = self.block_styling["max_row_size"] // 2
            grid.append([""] * padding + [last_val])

        fixed_grid = []
        for row in grid:
            new_rows = [row[i:i + self.block_styling["max_row_size"]] for i in
                        range(0, len(row), self.block_styling["max_row_size"])]
            fixed_grid += new_rows
        grid = fixed_grid

        if len(grid) == 0:
            grid_comp = GridPanel(1, 1, bg_color='White', bordered=block_styling['bordered'])
            self.add_component(grid_comp)
        else:
            # handle small grids
            if len(grid[0]) < self.block_styling["max_row_size"] and self.block_styling["fill_to_max_row"]:
                grid[0] += [""] * (self.block_styling["max_row_size"] - len(grid[0]))

            grid_comp = GridPanel(len(grid), len(grid[0]), bg_color='White', bordered=block_styling['bordered'])
            self.add_component(grid_comp)

            for i, row in enumerate(grid):
                for j, val in enumerate(row):
                    if type(val) == list:
                        val = StackPanel(val)
                    elif type(val) == str:
                        val = Label(val, size='md', bold=self.block_styling["bold_first_row"])
                    grid_comp.add_component(val, i, j)


class WikiButton(WikiBlock):
    DEFAULT_CONTENT = {
        "button_text": "כפתור",
        "button_func": None
    }

    def __init__(self, block_content=None, block_title=None, block_styling=None):
        if block_content is None:
            block_content = WikiButton.DEFAULT_CONTENT
        super().__init__(block_content=block_content, block_title=block_title, block_styling=block_styling)

        self.add_title()
        self.add_component(Button(self.block_content["button_text"], self.block_content["button_func"]))


class WikiUploader(WikiBlock):
    DEFAULT_TITLE = "העלאת קבצים"
    DEFAULT_CONTENT = {
        "drive_dir_id": None
    }

    def __init__(self, block_content=None, block_title=None, block_styling=None):
        if block_styling is None:
            block_styling = WikiForm.DEFAULT_STYLING
        if block_content is None:
            block_content = WikiForm.DEFAULT_CONTENT
        if block_title is None:
            block_title = WikiForm.DEFAULT_TITLE

        # Merge unspecified deafults
        block_content = {**WikiForm.DEFAULT_CONTENT, **block_content}
        self.google_drive = GoogleDrive.get_instance()
        self.files_upload = None
        super().__init__(block_content=block_content, block_title=block_title, block_styling=block_styling)

        self.add_title()

        file_panel = StackPanel([])

        # add drag n drop
        self.files_upload = UploadFiles(self.on_upload)
        file_panel.add_component(self.files_upload)

        # add button panel
        buttons_panel = StackPanel([], orientation=0)
        file_panel.add_component(buttons_panel)
        buttons_panel.add_component(Button('העלה קובץ', self.on_click))
        buttons_panel.add_component(Button('בטל', lambda *args: self.files_upload.update_files([])))

        self.add_component(file_panel)

    def on_click(self):
        count = 0
        for f_data in self.files_upload.get_files():
            f = FileToUpload.load_from_json(f_data)
            self.google_drive.upload_file_from_object(f, folder_id=self.block_content["drive_dir_id"])
            count += 1
        self.files_upload.update_files([])
        print(f"UPLOADED {count} files")

    def on_upload(self, files):
        self.files_upload.update_files(files)


class WikiFileDisplayer(WikiBlock):
    DEFAULT_TITLE = "קבצים בדף זה"
    DEFAULT_CONTENT = {
        "drive_dir_id": None
    }

    def __init__(self, block_content=None, block_title=None, block_styling=None):
        if block_styling is None:
            block_styling = WikiFileDisplayer.DEFAULT_STYLING
        if block_content is None:
            block_content = WikiFileDisplayer.DEFAULT_CONTENT
        if block_title is None:
            block_title = WikiFileDisplayer.DEFAULT_TITLE

        print("[INFO]\tDisplaying files")

        # Merge unspecified deafults
        block_content = {**WikiFileDisplayer.DEFAULT_CONTENT, **block_content}
        self.google_drive = GoogleDrive.get_instance()
        self.files_upload = None
        super().__init__(block_content=block_content, block_title=block_title, block_styling=block_styling)

        self.add_title()

        # read all the files from that drive dir id
        file_list = self.google_drive.list_files(
            folder_id=self.block_content["drive_dir_id"],
            no_folders=False
        )["files"]

        file_panel = StackPanel([])

        # add first link to that google drive link
        file_panel.add_component(HyperLink(
            text="קישור לתיקיית דרייב של דף זה",
            size="md",
            url=f"https://drive.google.com/drive/u/0/folders/{self.block_content['drive_dir_id']}"
        ))

        # add grid panel for all the files
        file_grid_width = 5
        files = self.display_file_list(file_list)

        file_panel.add_component(
            WikiGrid(
                block_content=[files],
                block_styling={
                    "max_row_size": file_grid_width,
                    "disp_title": False
                }
            )
        )

        self.add_component(file_panel)

        print("[INFO]\tFinished displaying files")

    def display_file_list(self, file_list):
        disp_list = []
        for file_data in file_list:
            if file_data["mimeType"] in ['application/vnd.google-apps.folder', 'application/vnd.google-apps.shortcut']:
                link_text = "קישור לתיקייה זו"
                link_url = f"https://drive.google.com/drive/u/0/folders/{file_data['id']}"
            else:
                link_text = "קישור לקובץ זה"
                link_url = f"https://drive.google.com/file/d/{file_data['id']}/view"

            file_data["url"] = link_url
            file_data["type"] = file_data["mimeType"]
            disp_list.append([
                DisplayFile(FileToUpload.load_from_json(file_data)),
                HyperLink(
                    text=link_text,
                    size="md",
                    url=link_url
                )
            ])
        return disp_list


class WikiForm(WikiBlock):
    DEFAULT_TITLE = "מצב עריכה"
    DEFAULT_CONTENT = {
        "form_model": BaseWikiPage,
        "value": None,
        "visible": ["name"],
        "display_name": constants.DEFAULT_DISPLAY_NAMES,
        "options": dict(),
        "options_display": dict(),
        "submit": None,
        "paragraphTexts": []
    }
    DEFAULT_STYLING = {
        "disp_title": False,
        "disp_form_title": True,
        "popup": True,
        "drive_dir_id": None
    }

    def __init__(self, block_content=None, block_title=None, block_styling=None):
        if block_styling is None:
            block_styling = WikiForm.DEFAULT_STYLING
        if block_content is None:
            block_content = WikiForm.DEFAULT_CONTENT
        if block_title is None:
            block_title = WikiForm.DEFAULT_TITLE

        # Merge unspecified deafults
        block_styling = {**WikiForm.DEFAULT_STYLING, **block_styling}
        block_content = {**WikiForm.DEFAULT_CONTENT, **block_content}

        super().__init__(block_content=block_content, block_title=block_title, block_styling=block_styling)

        self.add_title()

        # create panel for the popup
        popup_panel = StackPanel([])

        # Add file upload before if necessary
        if self.block_styling["drive_dir_id"] is not None:
            popup_panel.add_component(WikiDivider())
            popup_panel.add_component(WikiHeader(
                block_content="העלאת קבצים לדף",
                block_styling={
                    "size": "l",
                    "bold": True
                }
            ))
            popup_panel.add_component(WikiDivider())
            popup_panel.add_component(WikiUploader(
                block_content={
                    "drive_dir_id": self.block_styling["drive_dir_id"]
                }
            ))

        if self.block_styling["disp_form_title"]:
            popup_panel.add_component(WikiDivider())
            popup_panel.add_component(WikiHeader(
                block_content="עריכת תוכן הדף",
                block_styling={
                    "size": "l",
                    "bold": True
                }
            ))
            popup_panel.add_component(WikiDivider())

        popup_panel.add_component(JsonSchemaForm(
            self.block_content["form_model"],
            paragraphTexts=self.block_content["paragraphTexts"],
            value=self.block_content["value"],
            visible=self.block_content["visible"],
            display_name=self.block_content["display_name"],
            options=self.block_content["options"],
            options_display=self.block_content["options_display"],
            submit=self.block_content["submit"]
        ))

        if self.block_styling["popup"]:
            popup_panel = PopUp(popup_panel, title=self.block_title, is_shown=True, is_cancelable=True)

        self.add_component(popup_panel)


class WikiSearchBar(WikiBlock):
    DEFAULT_TITLE = "חפש עמודים"
    DEFAULT_CONTENT = {
        "refresh_callback": None
    }
    DEFAULT_STYLING = {
        "disp_title": True,
        "collapsible": False
    }

    def __init__(self, block_content=None, block_title=None, block_styling=None):
        if block_styling is None:
            block_styling = WikiSearchBar.DEFAULT_STYLING
        if block_content is None:
            block_content = WikiSearchBar.DEFAULT_CONTENT
        if block_title is None:
            block_title = WikiSearchBar.DEFAULT_TITLE

        super().__init__(block_content=block_content, block_title=block_title, block_styling=block_styling)

        print(block_styling)

        self.add_title()

        # add search bar
        form_panel = WikiForm(
            block_content={
                "visible": ["name"],
                "submit": lambda x: self.search(x),
            },
            block_styling={
                "disp_form_title": False,
                "popup": False,
                "drive_dir_id": None
            }
        )
        self.add_component(form_panel)

        # add spot for searched options
        self.search_panel = StackPanel([])
        self.search_panel.add_component(Label(""))
        self.add_component(self.search_panel)

        self.add_component(WikiDivider(block_styling={"long": True}))

    def search(self, x):
        top_pages = util.search_all_pages(x.name)

        self.search_panel.delete_component(0)
        self.search_panel.add_component(WikiGrid(
            block_content=self.create_search_options_grid(
                search_options=top_pages[:5],
                refresh_callback=self.block_content["refresh_callback"]
            ),
            block_styling={
                "disp_title": False,
                "bold_first_row": True,
                "fill_to_max_row": False
            }
        ))

    def create_search_options_grid(self, search_options, refresh_callback):
        pages_grid = []
        pages_grid.append(["אחוז התאמה %", "שם הדף", "מיקום בעץ", "סוג הדף", "מעבר לדף"])

        for i, option in enumerate(search_options):
            row = [
                Label(option[0], size='md'),
                Label(option[1].name, size='md', bold=True),
                Label(util.get_parents_path_str(option[1]), size='md'),
                Label(util.disp_name_from_type(option[1].__class__), size='md'),
                Button("עבור לדף", lambda x=option[1]: refresh_callback(x)),
            ]
            pages_grid.append(row)
        return pages_grid
