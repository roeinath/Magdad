from APIs.TalpiotAPIs import Tag
from APIs.TalpiotAPIs import TagList

from web_framework.server_side.infastructure.components.button import Button

import web_features.talpiwiki.constants as constants
import web_features.talpiwiki.util as util

import web_features.talpiwiki.talpiwiki_base as talpiwiki_base
import web_features.talpiwiki.wiki_components as wiki_components
from web_framework.server_side.infastructure.constants import *


class TalpiWikiMainPage(talpiwiki_base.TalpiWikiBasePage):
    def __init__(self, params):
        super().__init__(params)

        self.sp = None

    @staticmethod
    def get_title() -> str:
        return "ממשק הניהול"

    @staticmethod
    def is_authorized(user):
        return MATLAM in user.role  # Only the people of the base

    def draw_page(self):
        self.sp.clear()

        self.sp.add_component(wiki_components.WikiHeader(block_content="ממשק ניהול שימור הידע - תוכנית תלפיות"))

        self.sp.add_component(wiki_components.WikiDivider())

        self.sp.add_component(wiki_components.WikiGrid(
            block_content=self.create_page_grid(util.get_all_pages()),
            block_styling={
                "disp_title": True,
                "bold_first_row": True,
                'collapsible': True
            },
            block_title="רשימת דפים"
        ))

        self.sp.add_component(wiki_components.WikiButton(
            block_content={
                "button_text": "הוסף עמוד",
                "button_func": lambda: self.choose_page_type_popup(callback=self.create_page_popup)
            },
            block_styling={
                "disp_title": False
            }
        ))

        self.sp.add_component(wiki_components.WikiDivider())

        self.create_tag_lists()

        self.sp.add_component(wiki_components.WikiButton(
            block_content={
                "button_text": "צור תגית חדשה",
                "button_func": self.create_tag_popup
            },
            block_styling={
                "disp_title": False
            }
        ))

    def create_tag_lists(self):
        tag_lists = list(TagList.objects)

        for tag_list in tag_lists:
            self.sp.add_component(wiki_components.WikiGrid(
                block_content=self.create_tag_list_grid(tag_list),
                block_title=constants.DEFAULT_DISPLAY_NAMES[tag_list.name],
                block_styling={
                    "last_val_sep_row": True,
                    "collapsible": True
                }
            ))

    def create_tag_list_grid(self, tag_list):
        tag_names = [tag.name for tag in tag_list.taglist]
        return [tag_names + [Button("ערוך רשימה", lambda: self.edit_tag_list_popup(tag_list))]]

    def edit_tag_list_popup(self, tag_list):
        block_content = self.create_form_args(TagList)
        block_content["value"] = tag_list
        block_content["save_callback"] = self.refresh_page

        self.sp.add_component(wiki_components.WikiForm(
            block_content=block_content,
            block_styling={
                "edit_obj": True
            }
        ))

    def create_tag_popup(self):
        block_content = self.create_form_args(Tag)
        block_content["save_callback"] = self.refresh_page

        self.sp.add_component(wiki_components.WikiForm(
            block_content=block_content,
            block_styling={
                "edit_obj": False
            }
        ))


