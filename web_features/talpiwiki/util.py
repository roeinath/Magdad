from web_framework.server_side.infastructure.components.pop_up import PopUp
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.components.accordion import Accordion
from web_framework.server_side.infastructure.components.divider import Divider
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanel
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm
from web_framework.server_side.infastructure.components.document_grid_panel import DocumentGridPanelColumn
from fuzzywuzzy import fuzz

from APIs.TalpiotAPIs import *
from APIs.TalpiotAPIs import TagList

from APIs.TalpiotAPIs.Group.group import Group

import web_features.talpiwiki.constants as constants
from web_framework.server_side.infastructure.components.json_schema_form import JsonSchemaForm


# Special case: shana b -> leadership -> shabat hazon
# If has shabat hazon, we need to try to delete up until the root!
def delete_from_parents(node, event, mapping):
    for parent in node.parents:
        if event in mapping[parent]:
            mapping[parent].remove(event)
        delete_from_parents(parent, event, mapping)


def flatten(t):
    return [item for sublist in t for item in sublist]


def get_all_children_pages(page, curr_count=0):
    if curr_count >= 10:
        return []

    children_list = flatten([get_all_children_pages(child, curr_count + 1) for child in page.children])
    return [page] + children_list


def get_parents_path(page, curr_count=0):
    if len(page.parents) == 0:
        return [page.name]

    if curr_count >= 10:
        return ["max_depth"]

    # For now just take the top one
    return [page.name] + get_parents_path(page.parents[0], curr_count + 1)


def requery(page_node):
    return BaseWikiPage.objects(id=page_node.id)[0]


def get_parents_path_str(page):
    path_list = get_parents_path(page, 0)
    if "max_depth" in path_list:
        path = "מסלול מעגלי"
    else:
        path = " / ".join(reversed(path_list))
    return path


def remove_duplicates(all_nodes, mapping):
    for node in all_nodes:
        for event in mapping[node]:
            delete_from_parents(node, event, mapping)


# This functions goal is to match exisiting pages with events
def create_mapping(all_nodes, all_events, mapping):
    # If this is an end node, then children are empty and it will just return. already mapped.
    # We now want to suggest events for shibutz
    for node in all_nodes:
        mapping[node] = []
        for event in all_events:
            # This means it belongs even more to its child - more descriptive
            if node.name in event.title:
                # delete_from_parents(parent_node, event, mapping)
                mapping[node].append(event)


def get_all_pages():
    return list(BaseWikiPage.objects)


def search_all_pages(query):
    pages = get_all_pages()
    ratios = [(fuzz.token_set_ratio(query, page.name), page) for page in pages]
    ratios.sort(key=lambda x: x[0], reverse=True)
    return ratios


def get_all_groups():
    return list(Group.objects)


def get_main_page_node():
    pages = get_all_pages()

    if not len(pages):
        return None

    example_page = pages[0]
    while len(example_page.parents):
        example_page = example_page.parents[0]

    return example_page


def get_tags_by_list_name(name):
    tag_lists = list(TagList.objects)

    for tag_list in tag_lists:
        if tag_list.name == name:
            return tag_list.taglist

    # If tag name not found, return empty list
    return []


def get_prtty_hours(hours_float):
    return f'{"%.02f" % hours_float} שעות '


PAGE_TYPE_MAP = {
    "default": BaseWikiPage,
    "lecture": LecturePage,
    "event": EventPage,
    "platform": PlatformPage,
    "topic": TopicPage,
    "lecturer_page": LecturerPage,
    "year": YearPage,
    "activity": ActivityPage,
    "client_page": ClientPage,
    "project": ProjectPage
}


def get_page_name_from_type(type_class):
    revd = dict(map(reversed, PAGE_TYPE_MAP.items()))
    if type_class not in revd:
        return "default"
    return revd[type_class]


def disp_name_from_type(type_class):
    class_name = get_page_name_from_type(type_class)
    return constants.DEFAULT_DISPLAY_NAMES[class_name]
