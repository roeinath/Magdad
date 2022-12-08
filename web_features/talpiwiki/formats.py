from APIs.TalpiotAPIs import BaseWikiPage

# ALL_FIELDS = ["name", "parents", "children", "last_modified", "writer", "rational", "delete", "files"]

START_SHOW_COMMON = ["header", "name", "parents", "children", "last_modified", "writer", "edit"]
END_SHOW_COMMON = ["files", "calendar_suggestions"]

START_EDIT_COMMON = ["name", "page_type", "parents", "children", "last_modified", "writer"]
END_EDIT_COMMON = ["files"]

PAGE_TYPES = {
    "lecture": {
        "show": START_SHOW_COMMON + ["rational"] + END_SHOW_COMMON,
        "edit": START_EDIT_COMMON + ["rational"] + END_EDIT_COMMON
    },
    "lecturer": {
        "show": START_SHOW_COMMON + ["rational"] + END_SHOW_COMMON,
        "edit": START_EDIT_COMMON + ["rational"] + END_EDIT_COMMON
    },
    "event": {
        "show": START_SHOW_COMMON + ["rational"] + END_SHOW_COMMON,
        "edit": START_EDIT_COMMON + ["rational"] + END_EDIT_COMMON
    },
    "platform": {
        "show": START_SHOW_COMMON + ["rational"] + END_SHOW_COMMON,
        "edit": START_EDIT_COMMON + ["rational"] + END_EDIT_COMMON
    },
    "topic": {
        "show": START_SHOW_COMMON + ["rational"] + END_SHOW_COMMON,
        "edit": START_EDIT_COMMON + ["rational"] + END_EDIT_COMMON
    },
    "default": {
        "show": START_SHOW_COMMON + END_SHOW_COMMON,
        "edit": START_EDIT_COMMON + END_EDIT_COMMON
    }
}