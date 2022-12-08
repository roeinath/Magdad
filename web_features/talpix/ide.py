# from general import *
import os
from argparse import Action
import urllib.parse
import time

from mongoengine import Document, StringField
from APIs.TalpiotAPIs.Gitlab import update_file_tree
from APIs.TalpiotAPIs.Gitlab.gitlab_file_tree import GitlabFileTree
from APIs.TalpiotAPIs.Gitlab.update_file_tree import UpdateFileTree, GitlabAPI
from web_features.talpix import permissions
from web_framework.server_side.infastructure.components.all_components_import import FileTree, CodeEditor, Label, \
    Button, HyperLink, JsonSchemaForm, DocumentGridPanel, DocumentGridPanelColumn, ConfirmationButton,\
    CONFIRMATION_TEXT, PopUp, LogViewer, Markdown
from web_framework.server_side.infastructure.components.stack_panel import StackPanel, HORIZONTAL
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.ui_component import UIComponent
from ide_framework.site_container_side.development_feature import DevelopmentFeature
IDE_PAGE_URI = 'ide'
BASE_TEMPLATE = "bot_features/%s/%s/"


class IDE(Page):
    feature = DevelopmentFeature
    def __init__(self, params={}):
        super().__init__(params)
        self.path = None
        if len(params) > 0 and params[0] != 'undefined':
            self.path = params[0]
        self.sp = StackPanel([])
        self.editor_sp = StackPanel([])
        self.tree = None
        self.feature = None
        self.code_editor = None
        self.user = None
        self.popup = None

    @staticmethod
    def get_title() -> str:
        return "IDE"

    @staticmethod
    def is_authorized(user):
        return permissions.is_user_developer(user)

    def initiate_code_sp(self, path):
        self.sp.clear()
        self.code_editor = None
        self.sp.add_component(Label("IDE", fg_color=COLOR_PRIMARY_DARK, size=SIZE_EXTRA_LARGE))
        self.sp.add_component(Label(f"File: {path}", fg_color=COLOR_PRIMARY, size=SIZE_LARGE))
        # self.sp.add_component(HyperLink(f"לחצ/י כדי לקבל קישור",
        #                                 url=f"{IDE_PAGE_URI}/{urllib.parse.quote_plus(path)}"))
        content = self.feature.fetch_from_git(path)
        print("initiate_code_sp", path, content)
        print(path, '\n', content)
        self.code_editor = CodeEditor(content)
        print("heyyyyyy" + self.code_editor.get_code())
        self.path = path
        self.sp.add_component(self.code_editor)

        buttons_panel = StackPanel([], orientation=HORIZONTAL)

        if path.endswith('.py'):
            buttons_panel.add_component(Button("חזרה 🔙", bg_color='red', action=self.get_page_ui))
            buttons_panel.add_component(Button("שמירה 💾", action=self.save_button))
            buttons_panel.add_component(Button("הרצה 🏃", bg_color='green', action=self.run_button))
            buttons_panel.add_component(Button("קובץ חדש ➕", bg_color='orange', action=self.create_file_button))
            buttons_panel.add_component(ConfirmationButton("פרסום ⏫", bg_color='purple', action=self.publish_button))

        self.sp.add_component(buttons_panel)
        self.draw_tree()
        print("end" + self.code_editor.get_code())

    def change_file(self, path):
        if path.endswith('.py'):
            self.sp.delete_component(self.code_editor)
            buttons_sp = StackPanel([])
            buttons_sp.add_component(Button(f"move to {path}", action=lambda: self.initiate_code_sp(path)))
            buttons_sp.add_component(Button(f"delete {path}", action=lambda: self.delete_file_button(path)))
            self.popup = PopUp(buttons_sp, title="File changes", is_shown=True, is_cancelable=True)
            self.sp.add_component(self.popup)
            """self.sp.add_component(Button(f"move to {path}", action=lambda: self.initiate_code_sp(path)))"""

    def draw_terminal(self):
        logs_path = r'../../../../bot/src/ide_framework/feature_logs/log.txt'
        if os.path.isfile(logs_path):
            self.sp.add_component(LogViewer(logs_path))
        else:
            self.sp.add_component(CodeEditor("שגיאה בהצגת לוגים", language='text', theme='terminal'))

    def draw_tree(self):
        print("draw tree", self.feature.file_relative_paths)
        print(self.feature.feature_base_path)
        self.tree = FileTree(self.change_file , start_folder=self.feature.feature_name, branch=self.feature.branch_name)
        #self.sp.clear()
        #self.sp.add_component(Label("IDE", fg_color=COLOR_PRIMARY_DARK, size=SIZE_EXTRA_LARGE))
        self.sp.add_component(Label("בחר/י קובץ", size=SIZE_LARGE))
        self.sp.add_component(self.tree)

    def get_page_ui(self, user = None) -> UIComponent:
        #for obj in GitlabFileTree.objects(name='new_feature'):
        #    obj.delete()
        print("Start get_page_ui")
        if user is not None:
            self.user = user
            self.sp = StackPanel([])
        else:
            self.sp.clear()

        # TODO: add a column with delete feature button (delete from db, and close branch)
        features_component = DocumentGridPanel(
            DevelopmentFeature,
            column_list=[
                DocumentGridPanelColumn('feature_name', "פיצ'ר",
                                        component_parser=lambda row_data, feature_name: Label(feature_name))]
            ,filter_by={"users":self.user})
        features_component.add_column(lambda row_data: StackPanel([Button("פתח", action=lambda x = row_data: self.open_feature_button(x))]), title="")
        features_component.add_column(
            lambda row_data: StackPanel([Button("מחק", action=lambda x=row_data: self.yes_no_delete_feature_button(x))]),
            title="")
        # TODO: should be a button that triggers a popup with the JsonSchemaForm
        #  also, the form should ask more about the feature: where to put it for example
        self.sp.add_component(features_component)
        new_feature_button = Button("יצירת פיצ'ר חדש", action=self.create_feature_popup)
        self.sp.add_component(new_feature_button)
        print("end get_page_ui")

        return self.sp

    def publish_button(self):
        self.feature.publish()

    def save_button(self):
        self.feature.commit_and_push(self.code_editor.get_code(), self.path)

    def draw_run_stage(self):
        self.sp.clear()
        self.draw_terminal()
        buttons_sp = StackPanel([
            Button("חזרה 🔙", bg_color='red', action=lambda: self.initiate_code_sp(self.path)),
            ConfirmationButton("עצירת הרצה ⏸️", action=self.feature.stop_run),
            Button("טעינה 🔄", bg_color="green", action=self.draw_run_stage)
        ], orientation=HORIZONTAL)
        self.sp.add_component(buttons_sp)
        comment = "שימו לב: בלוגים האלה מופיעים בין היתר שגיאות של טלגרם שאין צורך לדאוג לגביהם"
        self.sp.add_component(Label(comment, size=SIZE_MEDIUM))

    def run_button(self):
        self.draw_run_stage()
        self.feature.run(self.code_editor.get_code())

    def delete_file_button(self, file_path):
        print('delete')
        self.feature.delete_file(file_path)
        self.popup.hide()
        self.initiate_code_sp(self.feature.file_relative_paths[0])

    def create_feature_popup(self):
        def submit_create_feature(ide_obj, feature_data):
            ide_obj.popup.hide()
            if feature_data.feature_name.replace('_', '').isalnum():
                ide_obj.create_feature_button(feature_data.feature_name, FeatureData.CATEGORY_MAPPING[feature_data.category], ide_obj.user)
                #ide_obj.yes_no_create_feature_button(feature_data.feature_name, FeatureData.CATEGORY_MAPPING[feature_data.category], ide_obj.user)
            else:
                ide_obj.sp.add_component(PopUp(Label("שם לא חוקי"), title='שגיאה', is_shown=True, is_cancelable=True))
        form = JsonSchemaForm(FeatureData, visible=['feature_name', 'category'], display_name={
            'feature_name': "פיצ'ר חדש",
            'category': "קטגוריה"
        }, placeholder={
            'feature': '',
            'category': 'בחר קטגוריה'
        }, options={
            'category': FeatureData.get_categories()
        },submit=lambda x: submit_create_feature(self, x))
        self.popup = PopUp(form, title="יצירת פיצ'ר חדש", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def create_feature_button(self, name, category, user):
        path = BASE_TEMPLATE%(category,name)# TODO add path
        self.feature = DevelopmentFeature.new_feature(name,user,path)
        self.initiate_code_sp(f"{self.feature.feature_name}.py")

    def yes_no_create_feature_button(self, name, category, user):
        self.sp.add_component(ConfirmationButton(text="האם את/ה בטוח/ה?", action=lambda _name=name, _category=category, _user=user: self.create_feature_button(_name, _category, _user)))

    def open_feature_button(self, feature):
        self.feature = feature
        path = f"{feature.feature_name}.py"  # TODO add path
        self.initiate_code_sp(path)

    def yes_no_delete_feature_button(self, feature):
        self.sp.add_component(ConfirmationButton(text=CONFIRMATION_TEXT, action=lambda _feature=feature: self.delete_feature_button(_feature)))

    def delete_feature_button(self, feature):
        feature.delete_feature()
        self.get_page_ui()

    def create_file_button(self):
        print("create file pressed")
        def submit_filename(filename_obj, ide_obj):
            print("submit pressed")
            ide_obj.popup.hide()
            ide_obj.feature.create_file(filename_obj.filename)
            self.initiate_code_sp(filename_obj.filename + '.py')
        form = JsonSchemaForm(FileName, visible=['filename'], display_name={'filename': 'שם הקובץ'},
                              placeholder={'filename': ''}, submit=lambda filename, ide_obj=self: submit_filename(filename, ide_obj))
        self.popup = PopUp(form, title='יצירת קובץ חדש', is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

class FileName(Document):
    filename = StringField()

class FeatureData(Document):
    CATEGORY_MAPPING = {'אחר': 'Other', 'אישי': 'Personal', 'מחזורי': 'Mahzori', 'שגרת מחנה': 'Shagmach', 'תכניתי': 'TalpiotGeneral'}
    feature_name = StringField()
    category = StringField()
    @staticmethod
    def get_categories():
        return ['אחר','אישי', 'מחזורי', 'שגרת מחנה', 'תכניתי']