# from general import *

from web_framework.server_side.infastructure.constants import *

from APIs.TalpiotAPIs import *

from APIs.TalpiotAPIs import PageType
from APIs.TalpiotAPIs import PageTypeChooser
from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs import Tag

from datetime import datetime
from datetime import timedelta

from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.page import Page

import web_features.talpiwiki.wiki_components as wiki_components
import web_features.talpiwiki.constants as constants
import web_features.talpiwiki.util as util
import web_features.talpiwiki.formats as formats

from APIs.ExternalAPIs import GoogleDrive
from APIs.ExternalAPIs import GoogleCalendar
# from APIs.ExternalAPIs import ScheduledJob

import time


class TalpiWikiBasePage(Page):
    def __init__(self, params):
        super().__init__()

        self.sp = None
        self.user = None
        self.wiki_comps = []

    def mark_interested(self, request):
        pass

    @staticmethod
    def is_authorized(user):
        return MATLAM in user.role  # Only the people of the base

    def show_filters(self):
        pass

    def get_page_ui(self, user):
        self.sp = StackPanel([])
        self.user = user
        self.draw_page()
        return self.sp

    def refresh_page(self, new_page_node=None):
        # Remove all existing UI
        self.sp.clear()

        # Draw the page again
        self.draw_page()

    @staticmethod
    def try_create_drive_folder(gd, page_node):
        try:
            if page_node.drive_dir_id is None or page_node.drive_dir_id == "":
                print(f"Creating Drive Folder for {page_node.name}")

                # Create folder under the default folder
                result = gd.create_folder(page_node.name, parent_ids=[constants.DEFAULT_SAVE_FOLDER_ID])
                page_node.drive_dir_id = result["id"]
                page_node.save()
        except Exception as e:
            print(f"Google Driver error when creating page: {e}")

    @staticmethod
    def try_move_drive_folder(gd, page_node):
        try:
            drive_parent_ids = gd.get_parent_ids(page_node.drive_dir_id)

            # Take drive ID of first parent
            wiki_parent_ids = constants.DEFAULT_SAVE_FOLDER_ID
            if len(page_node.parents):
                wiki_parent_ids = page_node.parents[0].drive_dir_id

            # Handle the root page seperately
            if page_node.name == "דף האב":
                wiki_parent_ids = constants.ROOT_PARENT_FOLDER_ID

            print(f"Comparing Drive IDS for {page_node.name}")
            print(drive_parent_ids)
            print(wiki_parent_ids)

            if drive_parent_ids != wiki_parent_ids:
                gd.move_drive_obj(
                    obj_id=page_node.drive_dir_id,
                    destination_folder=wiki_parent_ids
                )
        except Exception as e:
            print(f"Google Driver error when moving page: {e}")

    @staticmethod
    def organize_calendar():
        print("ORGANIZING CALENDAR\n")

        # Create directory if only doesnt exist
        for page_node in util.get_all_pages():
            page_node = util.requery(page_node)
            if page_node.calendar_id == "":
                continue

            time.sleep(1)

            with GoogleCalendar.get_instance() as gc:
                all_events = gc.get_events(
                    page_node.calendar_id,
                    start_time=datetime.now() - timedelta(weeks=50),
                    end_time=datetime.now() + timedelta(weeks=50),
                )

                # start by mapping all the nodes to the main node
                mapping = dict()
                util.create_mapping(list(BaseWikiPage.objects), all_events, mapping)

                # add default - all on root node
                mapping[page_node] = all_events

                util.remove_duplicates(list(BaseWikiPage.objects), mapping)

                # Save all these suggestions
                for page in mapping.keys():
                    page.events_title = [event.title for event in mapping[page]]
                    page.events_start = [event.start_time for event in mapping[page]]
                    page.events_end = [event.end_time for event in mapping[page]]
                    page.save()

    @staticmethod
    def organize_drive():
        print("ORGANIZING DRIVE\n")
        all_pages = util.get_all_pages()

        with GoogleDrive.get_instance() as gd:
            # Create drive folder id for everyone
            for page in all_pages:
                page = util.requery(page)
                TalpiWikiBasePage.try_create_drive_folder(gd, page)
                # time.sleep(1)

            # Organize everyone to be under their first parent
            for page in all_pages:
                page = util.requery(page)
                TalpiWikiBasePage.try_move_drive_folder(gd, page)
                # time.sleep(1)

    #
    # PAGE DB FUNCTIONS
    #

    @staticmethod
    def delete_page_from_db(page_node, also_drive=True):
        # add it as a child to all the parents
        for parent in page_node.parents:
            try:
                BaseWikiPage.objects(id=parent.id).update_one(pull__children=page_node.id)
            except Exception as e:
                print(f"Error when saving ids {e}")

        # add obj as parent to all children
        for child in page_node.children:
            try:
                BaseWikiPage.objects(id=child.id).update_one(pull__parents=page_node.id)
            except Exception as e:
                print(f"Error when saving ids {e}")

        # Try deleting from Drive as well
        try:
            if also_drive:
                with GoogleDrive.get_instance() as gd:
                    gd.move_drive_obj(
                        obj_id=page_node.drive_dir_id,
                        destination_folder=constants.DELETED_FOLDERS_DUMP
                    )
        except Exception as e:
            print(f"Google Driver error when deleting page: {e}")

        page_node.delete()

    @staticmethod
    def save_page_to_db(new_page):
        for parent in new_page.parents:
            BaseWikiPage.objects(id=parent.id).update_one(add_to_set__children=new_page.id)

        # add obj as parent to all children
        for child in new_page.children:
            BaseWikiPage.objects(id=child.id).update_one(add_to_set__parents=new_page.id)

        # Update drive data accordingly
        with GoogleDrive.get_instance() as gd:
            TalpiWikiBasePage.try_create_drive_folder(gd, new_page)
            TalpiWikiBasePage.try_move_drive_folder(gd, new_page)
            print("Renaming ", new_page.name)
            gd.rename_file(new_page.drive_dir_id, new_page.name)

    #
    # POPUP SEQUENCES
    #

    # Recvs 1 arg - callback function.
    # [INFO] Callback function - recvs 1 arg that is the chosen type
    def choose_page_type_popup(self, callback):
        self.create_default_page_types()
        page_types = list(PageType.objects)

        self.sp.add_component(wiki_components.WikiForm(
            block_content={
                "form_model": PageTypeChooser,
                "visible": ["page_types"],
                "display_name": {"page_types": "סוג הדף"},
                "options": {
                    "page_types": page_types,
                },
                "options_display": {
                    'page_types': lambda x: constants.DEFAULT_DISPLAY_NAMES[x.page_type]
                },
                "submit": lambda x: callback(
                    util.PAGE_TYPE_MAP[x.page_types.page_type]
                )
            },
        ))

    # Recvs 2 args - callback function, model_class class (chosen type)
    # [INFO] Callback function - recvs 1 arg, the filled in obj
    def create_page_popup(self, model_class, callback):
        block_content = self.create_form_args(model_class)

        block_content["submit"] = callback

        self.sp.add_component(wiki_components.WikiForm(
            block_content=block_content,
        ))

    # Recvs 2 args - callback function, and old page
    # [INFO] Callback function - recvs 1 arg, the filled in obj
    def edit_page_popup(self, model_page, callback):
        block_content = self.create_form_args(model_page.__class__)

        # add value from page
        block_content["value"] = model_page
        block_content["submit"] = callback

        self.sp.add_component(wiki_components.WikiForm(
            block_content=block_content,
            block_styling={
                "drive_dir_id": model_page.drive_dir_id
            }
        ))

    # Recvs 1 args - callback function
    # [INFO] Callback function - recvs no args!
    def delete_are_you_sure_popup(self, callback):
        self.sp.add_component(PopUp(
            StackPanel([
                Label(
                    "האם אתה בטוח שאתה רוצה למחוק דף זה?"
                ),
                Label(
                    "לידיעתך, שדות הדף יימחקו. קיימים גיבויים אצל צוות Talpix"
                ),
                Label(
                    "תיקיית הדרייב של עמוד זה (יחד עם כל בניה) תועבר ל'תיקיות מחוקות' בדרייב. יש לפנות למנהלי המערכת במידה ותרצו לגשת"
                ),
                Button(
                    "מחק דף",
                    lambda: callback(),
                    bg_color="red"
                )
            ]),
            title="אתה בטוח?", is_shown=True, is_cancelable=True
        ))

    # Recvs 0 args
    def you_are_restricted_popup(self):
        self.sp.add_component(PopUp(
            StackPanel([
                Label(
                    "אין לך הרשאות למחוק דף זה!"
                ),
                Label(
                    "יש לפנות למפתחי מערכת שימור הידע על מנת לקבל הרשאות"
                ),
            ]),
            title="חסרות הרשאות", is_shown=True, is_cancelable=True
        ))

    #
    # PAGE HANDLER FUNCTIONS
    #

    # Recvs 1 args - model page to delete
    def delete_page_handler(self, model_page=None):
        if model_page is None:
            return
        self.delete_page_from_db(model_page)

        self.refresh_page(new_page_node=util.get_main_page_node())

    # Recvs 2 args - form page, model class
    def create_page_handler(self, form_page, model_class):
        new_model_page = model_class()

        # Now take every visible attribute and set it in new_model_page
        for attr in model_class.visible:
            setattr(new_model_page, attr, getattr(form_page, attr, None))

        # create a new object with this data
        new_model_page.save()

        print(f"Saved object to DB {new_model_page}")

        TalpiWikiBasePage.save_page_to_db(new_model_page)

        self.refresh_page(new_page_node=new_model_page)

    # Recvs 2 args - form page, model page (existing_obj)
    def edit_page_handler(self, form_page, model_page):
        # Now take every visible attribute and set it in the exisitng object
        for attr in model_page.visible:
            setattr(model_page, attr, getattr(form_page, attr, getattr(model_page, attr, None)))
        model_page.save()

        TalpiWikiBasePage.save_page_to_db(model_page)

        self.refresh_page(new_page_node=model_page)

    # Recvs 2 args - model_class, model_page, (existing_obj)
    def convert_page_handler(self, model_class, model_page, duplicate=False):
        # get new obj class
        new_model_page = model_class()

        # copy all the attributes. The ones that dont exist will be copied into additional info
        more_fields = {}
        for attr in model_page.visible:
            attr_val = getattr(model_page, attr, None)

            if duplicate:
                if attr == "name":
                    attr_val += " (העתק) "
                if attr == "drive_dir_id":
                    attr_val = ""

            if attr in new_model_page.visible:
                setattr(new_model_page, attr, attr_val)
            else:
                more_fields[constants.DEFAULT_DISPLAY_NAMES[attr]] = attr_val

        # add all the additional info
        val = getattr(model_page, "additional_info", "")

        if len(more_fields):
            val += " --- "
            val += "שים לב! דף זה הומר לסוג דף חדש. בעבר דף זה היה מסוג "
            val += util.disp_name_from_type(model_page.__class__)
            val += " והומר לדף מסוג "
            val += util.disp_name_from_type(model_class)
            val += ". במהלך ההמרה, חלק מהשדות הקודמים נמחקו בשל שינוי הטיפוס." \
                   " שמרנו עבורך אותם במידה ויש בהם צורך, ייתכן והם ריקים. " \
                   "מומלץ לערוך / למחוק תוכן של שדה זה לאחר סיום העריכה. "
            val += str(more_fields)

        setattr(new_model_page, "additional_info", val)

        new_model_page.save()

        TalpiWikiBasePage.save_page_to_db(new_model_page)

        if not duplicate:
            TalpiWikiBasePage.delete_page_from_db(model_page, also_drive=False)

        print(f"Saved object to DB {new_model_page}")

        self.refresh_page(new_page_node=new_model_page)

    #
    # PAGE SEQUENCES
    #

    def create_page_sequence(self):
        self.choose_page_type_popup(
            callback=lambda model_class: self.create_page_popup(
                model_class=model_class,
                callback=lambda form_page: self.create_page_handler(
                    form_page=form_page,
                    model_class=model_class
                )
            )
        )

    def edit_page_sequence(self, model_page):
        self.edit_page_popup(
            model_page=model_page,
            callback=lambda form_page: self.edit_page_handler(
                form_page=form_page,
                model_page=model_page
            )
        )

    @staticmethod
    def restricted_page(model_page):
        if model_page.name in ["מטה", "דף האב", "שנה א", "שנה ב", "שנה ג"]:
            return True
        if model_page.__class__ == YearPage:
            return True
        return False

    @staticmethod
    def restricted_user(user):
        return user.name not in ["רועי זהר", "רועי טלמור", "רואי נבו מיכרובסקי","יואב פלטו"]

    def delete_page_sequence(self, model_page):
        if TalpiWikiBasePage.restricted_page(model_page) and TalpiWikiBasePage.restricted_user(self.user):
            self.you_are_restricted_popup()
        else:
            self.delete_are_you_sure_popup(
                callback=lambda: self.delete_page_handler(
                    model_page=model_page
                )
            )

    def convert_page_sequence(self, model_page):
        self.choose_page_type_popup(
            callback=lambda model_class: self.convert_page_handler(
                model_class=model_class,
                model_page=model_page
            )
        )

    def copy_page_sequence(self, model_page):
        self.convert_page_handler(
            model_class=model_page.__class__,
            model_page=model_page,
            duplicate=True
        )

    def create_page_grid(self, page_list=None):
        if page_list is None:
            page_list = []

        pages_grid = [["שם הדף", "סוג הדף", "תאריך עדכון אחרון", "כפתור עריכה", "כפתור מחיקה"]]

        for i, page in enumerate(page_list):
            row = [
                Label(page.name, size='md'),
                Label(page.__class__.__name__, size='md'),
                Label(page.last_modified, size='md'),
                Button("ערוך דף", lambda x=page: (self.edit_page_sequence(x))),
                Button("מחק דף", lambda x=page: (self.delete_page_sequence(x), self.refresh_page)),
            ]
            pages_grid.append(row)
        return pages_grid

    def create_default_page_types(self):
        # Delete everything in the database
        for obj in list(PageType.objects):
            obj.delete()

        # Create page types
        for page_type_name in util.PAGE_TYPE_MAP.keys():
            page_type_option = PageType(page_type=page_type_name)
            page_type_option.save()

    def create_form_args(self, page_class):
        pages = util.get_all_pages()
        groups = util.get_all_groups()
        lecturers = list(LecturerPage.objects)
        users = list(User.objects)
        page_types = formats.PAGE_TYPES.keys()
        tags = list(Tag.objects)
        clients = list(ClientPage.objects)

        # tag lists
        content_tags = util.get_tags_by_list_name("content_tags")
        logistic_tags = util.get_tags_by_list_name("logistic_tags")
        bakara_tags = util.get_tags_by_list_name("bakara_tags")
        projectal_tags = util.get_tags_by_list_name("projectal_tags")

        block_content = {
            "form_model": page_class,
            "paragraphTexts": constants.PARAGRAPH_TEXTS,
            "visible": page_class.visible,
            "options": {
                "bakara_tags": bakara_tags,
                "logistic_tags": logistic_tags,
                "content_tags": content_tags,
                "projectal_tags": projectal_tags,
                "taglist": tags,
                'writer': users,
                'children': pages,
                'parents': pages,
                "page_type": page_types,
                "audience": groups,
                "lecturer": lecturers,
                "organizers": users,
                "recommendation": constants.RECOMMANDATIONS,
                "client": clients
            },
            "options_display": {
                "bakara_tags": lambda x: x.name,
                "logistic_tags": lambda x: x.name,
                "content_tags": lambda x: x.name,
                "projectal_tags": lambda x: x.name,
                "taglist": lambda x: x.name,
                'writer': lambda x: x.name,
                'children': lambda x: x.name,
                'parents': lambda x: x.name,
                'page_type': lambda x: x,
                "audience": lambda x: x.name,
                "lecturer": lambda x: x.name,
                "organizers": lambda x: x.name,
                'recommendation': lambda x: x,
                "client": lambda x: x.name
            },
        }
        return block_content

    #
    # Page handler helper functions
    #

    def draw_page(self):
        pass


def create_job_list():
    return
    # jobs = list()
    # jobs.append(ScheduledJob(
    #     method=TalpiWikiBasePage.organize_drive,
    #     minute=f"*/{constants.ORGANIZING_INTERVAL}"
    # ))
    # jobs.append(ScheduledJob(
    #     method=TalpiWikiBasePage.organize_calendar,
    #     minute=f"*/{constants.ORGANIZING_INTERVAL}"
    # ))
    # jobs[0].schedule()
    # jobs[1].schedule()

create_job_list()
# TalpiWikiBasePage.organize_drive()
