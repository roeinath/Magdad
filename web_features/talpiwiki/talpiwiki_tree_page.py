from datetime import date

from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.label import Label

import web_features.talpiwiki.constants as constants
import web_features.talpiwiki.util as util

import web_features.talpiwiki.talpiwiki_base as talpiwiki_base
import web_features.talpiwiki.wiki_components as wiki_components
from web_framework.server_side.infastructure.constants import *
from APIs.ExternalAPIs import GoogleDrive


class TalpiWikiTreePage(talpiwiki_base.TalpiWikiBasePage):
    def __init__(self, params, page_node=None):
        super().__init__(params)

        self.page_node = page_node
        if page_node is None:
            self.page_node = util.get_main_page_node()

        self.sp = None

    def mark_interested(self, request):
        pass

    @staticmethod
    def get_title() -> str:
        return "עץ ההכשרה"

    @staticmethod
    def is_authorized(user):
        return MATLAM in user.role  # Only the people of the base

    def refresh_page(self, new_page_node=None):
        # Remove all existing UI
        self.sp.clear()

        # Change the current node
        if new_page_node is not None:
            self.page_node = new_page_node

        self.page_node = util.requery(self.page_node)

        # Draw the page again
        self.draw_page()

    # Auto mapping from every wiki page attribute to it's description
    # block_content is a function that returns the content for that block, and gets the self, page node as a parameter

    WIKI_PAGE_MAPPING = {
        "header": {
            "wiki_component": wiki_components.WikiHeader,
            "wiki_args": {
                "block_content": lambda self: "עץ ההכשרה שימור הידע - תוכנית תלפיות",
                "block_styling": lambda self: {
                    "size": "l"
                }
            }
        },
        "name": {
            "wiki_component": wiki_components.WikiHeader,
            "wiki_args": {
                "block_title": lambda self: "שם הדף",
                "block_content": lambda self: self.page_node.name
            }
        },
        "explanation": {
            "wiki_component": wiki_components.WikiOneLiner,
            "wiki_args": {
                "block_title": lambda self: "שם הדף",
                "block_content": lambda self: self.explanation_content(),
                "block_styling": lambda self: {
                    "disp_title": False
                }
            }
        },
        "writer": {
            "wiki_component": wiki_components.WikiOneLiner,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["writer"],
                "block_content": lambda self: [writer.name for writer in self.page_node.writer],
            }
        },
        "organizers": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["organizers"],
                "block_content": lambda self: [page.name for page in self.page_node.organizers],
            }
        },
        "last_modified": {
            "wiki_component": wiki_components.WikiOneLiner,
            "wiki_args": {
                "block_title": lambda self: "תאריך עדכון אחרון",
                "block_content": lambda self: self.page_node.last_modified,
            }
        },
        "parents": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: "דפים מעליו",
                "block_content": lambda self: self.create_page_node_link_list(self.page_node.parents,
                                                                              above=constants.NO_BUTTON),
                "block_styling": lambda self: {
                    "bordered": False
                }
            }
        },
        "children": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: "דפים תחתיו",
                "block_content": lambda self: self.create_page_node_link_list(self.page_node.children,
                                                                              above=constants.NO_BUTTON),
                "block_styling": lambda self: {
                    "bordered": False
                }
            }
        },
        "rational": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": {
                "block_title": lambda self: "רציונל הכשרתי",
                "block_content": lambda self: self.page_node.rational,
            }
        },
        "files": {
            "wiki_component": wiki_components.WikiFileDisplayer,
            "wiki_args": {
                "block_content": lambda self: {
                    "drive_dir_id": self.page_node.drive_dir_id
                }
            }
        },
        "event_data": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: "אירועים משוייכים" + f" ({len(self.get_all_events())})",
                "block_content": lambda self: self.create_calendar_grid(),
            }
        },
        "overall_grade": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "summary": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "lecturer": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["lecturer"],
                "block_content": lambda self: self.create_page_node_link_list(self.page_node.lecturer,
                                                                              above=constants.NO_BUTTON)
            }
        },
        "goals": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": "default"
        },
        "logic_line": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "phone_num": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "background": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "feedback": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "price": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "email": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "lecturer_color": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "omes_grid": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": {
                "block_title": lambda self: "טבלת עומסים אוטומטית (פיצ'ר בבנייה)",
                "block_content": lambda self: self.create_omes_grid(),
            }
        },
        "edit": {
            "wiki_component": wiki_components.WikiButton,
            "wiki_args": {
                "block_title": lambda self: "עריכת עמוד זה",
                "block_content": lambda self: {
                    "button_text": "עריכת עמוד זה",
                    "button_func": lambda: self.edit_page_sequence(self.page_node),
                },
                "block_styling": lambda self: {
                    "disp_title": False,
                }
            }
        },
        "recommendation": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": {
                "block_content": lambda self: getattr(self.page_node, "recommendation", ""),
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["recommendation"],
                "block_styling": lambda self: {
                    "disp_title": True,
                    "bg_map": constants.RECOMMENDATION_BG_MAP
                }
            }
        },
        "status": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": {
                "block_content": lambda self: getattr(self.page_node, "status", ""),
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["status"],
                "block_styling": lambda self: {
                    "disp_title": True,
                    "bg_map": constants.STATUSES_BG_MAP
                }
            }
        },
        "budget_id": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "past_lectures": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["past_lectures"],
                "block_content": lambda self: self.display_lectures(),
                "block_styling": lambda self: {
                    "bold_first_row": True,
                    "max_row_size": 4
                }
            }
        },
        "project_list": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["project_list"],
                "block_content": lambda self: self.display_projects(),
                "block_styling": lambda self: {
                    "bold_first_row": True,
                    "max_row_size": 5
                }
            }
        },
        "bakara_tags": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["bakara_tags"],
                "block_content": lambda self: [tag.name for tag in self.page_node.bakara_tags],
            }
        },
        "logistic_tags": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["logistic_tags"],
                "block_content": lambda self: [tag.name for tag in self.page_node.logistic_tags],
            }
        },
        "content_tags": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["content_tags"],
                "block_content": lambda self: [tag.name for tag in self.page_node.content_tags],
            }
        },
        "projectal_tags": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["projectal_tags"],
                "block_content": lambda self: [tag.name for tag in self.page_node.projectal_tags],
            }
        },
        "divider": {
            "wiki_component": wiki_components.WikiDivider,
            "wiki_args": "default"
        },
        "additional_info": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "responsibilities": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": "default"
        },
        "conclusions": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": "default"
        },
        "core_values": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": "default"
        },
        "output_calendar": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["output_calendar"],
                "block_content": lambda self: "חלק זה ייצר קלנדר בלעדי על סמך הדפים הנמצאים תחתיו, עדיין בפיתוח",
            }
        },
        "client": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["client"],
                "block_content": lambda self: self.create_page_node_link_list(self.page_node.client,
                                                                              above=constants.NO_BUTTON)
            }
        },
        "connection_with_client": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "contact_details": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "technologichal": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "good_projects": {
            "wiki_component": wiki_components.WikiParagraph,
            "wiki_args": "default"
        },
        "search_bar": {
            "wiki_component": wiki_components.WikiSearchBar,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["search_bar"],
                "block_content": lambda self: {
                    "refresh_callback": lambda x, s=self: s.refresh_page(x)
                }
            }
        },
        "control_bar": {
            "wiki_component": wiki_components.WikiGrid,
            "wiki_args": {
                "block_title": lambda self: constants.DEFAULT_DISPLAY_NAMES["control_bar"],
                "block_content": lambda self: self.create_control_bar(),
                "block_styling": lambda self: {
                    "disp_title": False,
                    "bordered": False,
                    "max_row_size": 6
                }
            }
        }
    }

    def create_control_bar(self):
        control_bar = []
        control_bar.append(Button(
            "🔄 רענן עמוד זה",
            lambda: self.refresh_page(),
            bg_color="gray"
        ))
        control_bar.append(Button(
            "➕ צור עמוד תחת עמוד זה",
            lambda: self.create_page_sequence(),
            bg_color="gray"
        ))
        control_bar.append(Button(
            "✍🏻 ערוך עמוד זה",
            lambda: self.edit_page_sequence(self.page_node),
            bg_color="gray"
        ))
        control_bar.append(Button(
            "↩️ המר עמוד זה",
            lambda: self.convert_page_sequence(self.page_node),
            bg_color="gray"
        ))
        control_bar.append(Button(
            "🗐 העתק עמוד זה",
            lambda: self.copy_page_sequence(self.page_node),
            bg_color="gray"
        ))
        control_bar.append(Button(
            "🗑️ מחק עמוד זה",
            lambda: self.delete_page_sequence(self.page_node),
            bg_color="gray"
        ))

        return control_bar

    def explanation_content(self):
        path = util.get_parents_path_str(self.page_node)
        class_name = util.get_page_name_from_type(self.page_node.__class__)
        path += f" - {constants.DEFAULT_DISPLAY_NAMES[class_name]}"
        return path

    def upload_files_popup(self):
        self.sp.add_component(wiki_components.WikiUploader())

    def get_relevant_pages(self, field="lecturer"):
        # Assumes current page node is a lecturer
        pages = util.get_all_pages()

        # find all pages that have our lecturer in them
        relevant_pages = []
        for page in pages:
            if self.page_node in getattr(page, field, []):
                relevant_pages.append(page)

        return relevant_pages

    def display_lectures(self):
        lectures = self.get_relevant_pages(field="lecturer")

        pages_grid = [["שם ההרצאה", "סיכום", "המלצה", "מעבר להרצאה"]]

        for i, lecture in enumerate(lectures):
            row = [
                Label(lecture.name, size='md'),
                Label(lecture.summary, size='md'),
                Label(lecture.recommendation, size='md',
                      bg_color=constants.RECOMMENDATION_BG_MAP.get(lecture.recommendation, None)),
                Button("עבור להרצאה", lambda x=lecture: self.refresh_page(new_page_node=x)),
            ]
            pages_grid.append(row)
        return pages_grid

    def display_projects(self):
        projects = self.get_relevant_pages(field="client")

        pages_grid = [["שם הפרויקט", "תקציר הפרויקט", "קשר עם הלקוח", "סטטוס", "מעבר לפרויקט"]]

        for i, project in enumerate(projects):
            row = [
                Label(project.name, size='md'),
                Label(project.summary, size='md'),
                Label(project.connection_with_client, size='md'),
                Label(project.status, size='md',
                      bg_color=constants.STATUSES_BG_MAP.get(project.status, None)),
                Button("עבור לפרויקט", lambda x=project: self.refresh_page(new_page_node=x)),
            ]
            pages_grid.append(row)
        return pages_grid

    def create_form_args(self, page_class):
        block_content = super().create_form_args(page_class)

        parents = [self.page_node]

        # add defaults based on where you are in the tree
        block_content["value"] = page_class(
            name="שם הדף",
            writer=[self.user],
            audience=self.page_node.audience,
            last_modified=date.today(),
            parents=parents
        )
        return block_content

    def create_calendar_grid(self):
        print("[INFO]\tDisplaying Calendar")

        if len(self.page_node.events_title):
            suggestion_list = [
                StackPanel([
                    Label(f'{event_data["title"]}\n', size="md", bold=True),
                    Label(f'אורך - {util.get_prtty_hours(event_data["length"])}', size="md"),
                ])
                for event_data in sorted(self.get_all_events(), key=lambda x: x["event_start"])
            ]
        else:
            suggestion_list = [
                Label("לא נמצאו אירועים רלוונטיים בקלנדר", size="md")
            ]

        print("[INFO]\tFinished Displaying Calendar")
        return suggestion_list

    @staticmethod
    def filter_event_list(event_list):
        filtered = filter(lambda x: x["length"] < 12, event_list)
        return list(filtered)

    def get_all_events(self, filter=True):
        # get all children
        all_children = util.get_all_children_pages(self.page_node)

        # get all events
        all_events = [{
            "title": event_title,
            "length": (event_end - event_start).total_seconds() / 3600,
            "event_start": event_start
        }
            for child in all_children
            for (event_title, event_start, event_end)
            in zip(child.events_title, child.events_start, child.events_end)
        ]

        if filter:
            all_events = TalpiWikiTreePage.filter_event_list(all_events)

        return all_events

    def create_omes_grid(self):
        all_events = self.get_all_events()

        # get all hours
        all_hours = sum([event["length"] for event in all_events])

        return "סך השעת בתת העץ: " + util.get_prtty_hours(all_hours)

    def create_page_node_link_list(self, page_nodes, above=constants.NO_BUTTON):
        existing = [
            Button(
                page_node.name,
                lambda p=page_node: self.refresh_page(p),
                bg_color=constants.PAGE_TYPE_BG_MAP[
                    util.get_page_name_from_type(page_node.__class__)
                ]
            )
            for i, page_node in enumerate(sorted(page_nodes, key=lambda x: x.name))
        ]

        if above != constants.NO_BUTTON:
            existing.append(
                Button(
                    "הוספת עמוד",
                    lambda: self.choose_page_type_popup(
                        callback=lambda x: self.create_page_popup(x, above=False)
                    ),
                )
            )
        return existing

    def draw_page(self):
        # If no current page is associated
        if self.page_node is None:
            return

        try:
            gd = GoogleDrive.get_instance()
            gd.list_files()
        except Exception as e:
            print("ERROR: couldn't connect to drive " + str(e))
            self.sp.add_component(Label("בעייה בחיבור לדרייב - יש לחדש את הtoken", bg_color='red'))
            return

        # Draw the wiki page
        NO_DISP_LIST = ["omes_grid", "event_data"]

        for block_attr in self.page_node.__class__.displayed:
            if block_attr in NO_DISP_LIST:
                continue

            print(f"Displaying {block_attr}")

            block_args = TalpiWikiTreePage.WIKI_PAGE_MAPPING[block_attr]["wiki_args"]

            args = dict()
            if block_args == "default":
                args["block_content"] = getattr(self.page_node, block_attr, "")
                args["block_title"] = constants.DEFAULT_DISPLAY_NAMES[block_attr]

            else:
                if "block_content" in block_args.keys():
                    args["block_content"] = block_args["block_content"](self)
                if "block_title" in block_args.keys():
                    args["block_title"] = block_args["block_title"](self)
                if "block_styling" in block_args.keys():
                    args["block_styling"] = block_args["block_styling"](self)

            self.sp.add_component(TalpiWikiTreePage.WIKI_PAGE_MAPPING[block_attr]["wiki_component"](**args))
