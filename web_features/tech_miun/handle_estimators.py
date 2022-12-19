from mongoengine import *

from APIs.TalpiotAPIs import User
from web_features.groups.add_users_from_csv import add_users_from_csv
from web_features.tech_miun import permissions
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanel, \
    DocumentGridPanelColumn
from web_framework.server_side.infastructure.components.hyper_link import HyperLink
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.stack_panel import StackPanel, HORIZONTAL
from web_framework.server_side.infastructure.components.upload_files import UploadFiles
from web_framework.server_side.infastructure.constants import *
from web_framework.server_side.infastructure.page import Page

ADD_USERS_URL = r"https://drive.google.com/file/d/1KrWhrVx6gGkEASi-6l9wCSUNHkztCD6D/view"
TITLE = "ניהול הרשאות מיון"


class HandleEstimators(Page):
    @staticmethod
    def get_title() -> str:
        return TITLE

    @staticmethod
    def is_authorized(user: User):
        return permissions.is_master_miun(user)

    def __init__(self, params):
        super().__init__()
        self.sp: StackPanel = None
        self.popup: PopUp = None
        self.user = None

    def get_page_ui(self, user):
        self.sp = StackPanel([])
        self.user = user
        self.draw()
        return self.sp

    def draw(self):
        """
        Draws the page UI: a grid with all the users and their permissions and a button to add new users from a csv file
        :return: None
        """
        self.sp.clear()
        self.sp.add_component(Label(TITLE, size=SIZE_EXTRA_LARGE, fg_color=COLOR_PRIMARY_DARK))

        self.sp.add_component(DocumentGridPanel(User, [
            DocumentGridPanelColumn("name", "שם"),
            DocumentGridPanelColumn("email", "אימייל"),
            DocumentGridPanelColumn("phone_number", "טלפון"),
            DocumentGridPanelColumn("role", "תפקידים"),
            DocumentGridPanelColumn("name", " ", lambda user, _: Button("עריכה", lambda: self.edit_user(user)))
        ], filter_by={'role__in': permissions.ALL_MIUN_ROLES}))

        self.sp.add_component(Divider())

        buttons_sp = StackPanel([
            Button(f"הוספת מורשים", self.add_permissions_for_miun, bg_color='green'),
            Button(f"הורדת הרשאות", self.remove_permissions_for_miun, bg_color='red')
        ], orientation=HORIZONTAL)
        self.sp.add_component(buttons_sp)

        self.sp.add_component(Divider())
        self.sp.add_component(Button(f"הוספת משתמשים מקובץ CSV", self.create_miun_users_from_csv))
        self.sp.add_component(HyperLink('פורמט קובץ להוספת משתמשים', bold=True, url=ADD_USERS_URL))

    def edit_user(self, user):
        """
        Opens a popup with a form to edit the user
        :param user: User object
        :return: None
        """

        def save_user(obj):
            user.email = obj.email
            user.name = obj.name
            user.phone_number = obj.phone_number
            user.save()
            self.popup.hide()
            self.draw()

        FORMS_FIELDS = {'email': 'מייל', 'name': 'שם', 'phone_number': 'טלפון'}
        form = JsonSchemaForm(User, value=user, visible=list(FORMS_FIELDS.keys()), display_name=FORMS_FIELDS,
                              options={}, options_display={}, submit=save_user)
        self.popup = PopUp(form, title="עריכת משתמש/ת", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def edit_permissions_for_miun(self, title, handle_group_schema):
        """
        Opens a popup with a form to change the permissions of a user group (add or remove)
        :param title: str - the title of the popup
        :param handle_group_schema: method - the method to apply on the users
        :return: None
        """

        def on_submit(group: GroupSchema):
            handle_group_schema(group)
            self.popup.hide()
            self.draw()

        form = JsonSchemaForm(
            GroupSchema,
            visible=GroupSchema.FORM_FIELDS,
            display_name=GroupSchema.display_name_dict_fields,
            options=GroupSchema.options_dict_fields,
            options_display=GroupSchema.options_display_dict_fields,
            submit=on_submit
        )

        self.popup = PopUp(form, title=title, is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def add_permissions_for_miun(self):
        """
        Opens a popup with a form to add permissions to a user group
        :return: None
        """

        def add_permissions_to_group(group: GroupSchema):
            for user in group.participants:
                if group.miun_type not in user.role:
                    user.role.append(group.miun_type)
                    user.save()

        self.edit_permissions_for_miun("הוספת הרשאות מיון ✅", add_permissions_to_group)

    def remove_permissions_for_miun(self):
        """
        Opens a popup with a form to remove permissions from a user group
        :return: None
        """

        def remove_permissions_to_group(group: GroupSchema):
            for user in group.participants:
                if group.miun_type in user.role:
                    user.role.remove(group.miun_type)
                    user.save()

        self.edit_permissions_for_miun("הורדת הרשאות מיון ❌", remove_permissions_to_group)

    def create_miun_users_from_csv(self):
        """
        Opens a popup with a form to add users from a csv file and give them permissions
        :return: None
        """

        def set_miun_type(chosen_miun_type):
            self.popup.hide()
            self.sp.delete_component(self.popup)
            upload_file = UploadFiles(lambda file: self.add_miun_users_from_csv(file, chosen_miun_type.miun_type))
            self.popup = PopUp(upload_file, title="העלאת קובץ CSV", is_shown=True, is_cancelable=True)
            self.sp.add_component(self.popup)

        form = JsonSchemaForm(GroupSchema, value=GroupSchema(miun_type=permissions.ESTIMATOR_MIUN),
                              visible=['miun_type'], display_name={'miun_type': 'סוג הרשאות'},
                              options={'miun_type': permissions.ALL_MIUN_ROLES},
                              options_display={'miun_type': lambda x: x}, submit=set_miun_type)

        self.popup = PopUp(form, title="בחירת סוג הרשאות", is_shown=True, is_cancelable=True)
        self.sp.add_component(self.popup)

    def add_miun_users_from_csv(self, files, miun_type):
        """
        Adds users from a csv file and gives them permissions
        :param files: list of files uploaded - only the first file is used
        :param miun_type: str - the type of permissions to give to the users
        :return: None
        """
        participants = []
        add_users_from_csv(files[0], participants, remove_numer=False)
        for participant in participants:
            participant.role.append(miun_type)
            participant.role.remove(MATLAM)
            participant.save()
        self.popup.hide()
        self.draw()


class GroupSchema(Document):
    miun_type = StringField()
    participants = ListField(ReferenceField(User))

    FORM_FIELDS = ['miun_type', 'participants']
    FORM_DISPLAY = ['סוג הרשאות', 'משתמשים']
    FORM_OPTIONS = [permissions.ALL_MIUN_ROLES, User.objects]
    FORM_OPTIONS_DISPLAY = [lambda x: x, lambda user: user.get_full_name()]

    display_name_dict_fields = dict(zip(FORM_FIELDS, FORM_DISPLAY))
    options_dict_fields = dict(zip(FORM_FIELDS, FORM_OPTIONS))
    options_display_dict_fields = dict(zip(FORM_FIELDS, FORM_OPTIONS_DISPLAY))
