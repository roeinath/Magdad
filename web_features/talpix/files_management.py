# from general import *

from APIs.ExternalAPIs.FilesAPIs.talpix_file import TalpiXFile

from APIs.TalpiotAPIs.User.user import User
from web_framework.server_side.infastructure.components.download_button import DownloadButton
from web_framework.server_side.infastructure.components.file_uploader import FileUploader
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.ui_component import UIComponent
from web_framework.server_side.infastructure.constants import *

class FilesManager(Page):
    def __init__(self, params={}):
        super().__init__(params)
        self.sp = StackPanel([])

    @staticmethod
    def get_title() -> str:
        return "קבצים אישיים"

    @staticmethod
    def is_authorized(user):
        return MATLAM in user.role  # Only the people of the base

    def manage_shared_with(self, file):
        def save_file(new_file):
            file.shared_with = new_file.shared_with
            self.popup.hide()
            file.save()

        form = JsonSchemaForm(TalpiXFile, visible=["shared_with"], 
            value=file,
            display_name={
                'shared_with': 'משתמשים משותפים',
            }, 
            placeholder={
            },
            options={
                'shared_with': User.objects,
            }, 
            options_display= {
                'shared_with': lambda x: x.name + "-" + str(x.mahzor),
            }, 
            submit=save_file)

        self.popup = PopUp(form, title="עריכת קובץ", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def share_with_group(self, file):
        
        self.popup = PopUp(Label("הפיצ'ר עוד לא קיים"), title='בבנייה', is_shown=True, is_cancelable=True)
        self.sp.add_action(self.popup)

    def delete(self, file):
        pass


    def draw_table(self):
        self.sp.clear()
        self.sp.add_component(FileUploader(upload_owner=self.user))

        files = TalpiXFile.objects(owner=self.user)
        table = GridPanel(len(files), 5)
        for i, file in enumerate(files):
            table.add_component(Label(file.filename), i, 0)
            table.add_component(DownloadButton("הורד", file, bg_color='green'), i, 1)
            table.add_component(Button("הגדרות שיתוף", lambda f=file: self.manage_shared_with(f)), i, 2)
            table.add_component(Button("שיתוף עם קבוצה (עוד לא עובד)", lambda f=file: self.share_with_group(f)), i, 3)
            table.add_component(Button("מחק", lambda f=file: self.delete(f), bg_color='red'), i, 4)
        self.sp.add_component(Label("קבצים שלי"))
        self.sp.add_component(table)

        files = TalpiXFile.objects(shared_with=self.user)
        table = GridPanel(len(files), 2)
        for i, file in enumerate(files):
            table.add_component(Label(file.filename), i, 0)
            table.add_component(DownloadButton("הורד", file, bg_color='green'), i, 1)
        self.sp.add_component(Label("קבצים ששותפו איתי"))
        self.sp.add_component(table)

    def get_page_ui(self, user) -> UIComponent:
        self.user = user

        self.sp = StackPanel([])
        self.draw_table()

        return self.sp
