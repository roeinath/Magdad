from web_framework.server_side.infastructure.page import Page
# standard Talpix page class to inherit from.
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_features.Elements.personal_page.modules.cadet_classes import *
from web_features.Elements.personal_page.permissions import *
from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.constants import *

RealData = TalpiotSettings.is_master()


class CadetPage(Page):
    """
    This page contains data of single cadets for commanders - skirot and academia
    """

    def __init__(self, params):
        super().__init__(params)
        self.gp = GridPanel(5, 1, bordered=False)
        self.selected_mahzor = None
        self.selected_cadet = None
        self.mahzor_names = {}

    @staticmethod
    def get_title():
        return "נתוני צוערים"

    @staticmethod
    def is_authorized(user):
        return MATLAM in user.role  # Only the people of the base

    def get_page_ui(self, user: User):
        self.user = user

        self.gp.add_component(Label("צפייה בציוני צוערים", size=SIZE_EXTRA_LARGE), 0, 0)

        self.options_layout = GridPanel(2, 2, bg_color=COLOR_PRIMARY_DARK)

        # Labels
        self.options_layout.add_component(Label("מחזור", fg_color='White'), 0, 1)
        self.options_layout.add_component(Label("צוער", fg_color='White'), 0, 0)

        # Options
        self.mahzor_combo = ComboBox(mahzor_numstr_to_letters,
                                     on_changed=lambda selected_mahzor: self.load_cadet_combo_box(selected_mahzor),
                                     default_value=str(self.user.mahzor))

        # Just default for init - changes in load_cadet_combo_box
        name_utils = {str(u.name): str(u.name) for u in User.objects(mahzor=user.mahzor)}
        self.cadet_combo_box = ComboBox(name_utils, on_changed=lambda cadet: self.change_cadet(cadet),
                                        default_value=self.user.name)

        self.options_layout.add_component(self.mahzor_combo, 1, 1)
        self.options_layout.add_component(self.cadet_combo_box, 1, 0)
        self.gp.add_component(self.options_layout, 1, 0)

        # load grades for user when he opens the page
        if not (is_user_captain(self.user)) and self.selected_cadet is None:
            # self.load_cadet_combo_box(self.user.mahzor)
            self.selected_mahzor = int(self.user.mahzor)
            self.change_cadet(self.user.name)

        return self.gp

    def load_cadet_combo_box(self, mahzor):
        """
        called after choosing a mahzor. loads the relevant cadets for the user
        """
        self.selected_mahzor = int(mahzor)
        self.mahzor_names = {}
        # each person can see another persons grades

        # TODO: check if can do generic with talpix
        for cadet in User.objects(mahzor=self.selected_mahzor):
            cadet_name = cadet.name
            if is_user_have_permissions(using_user=self.user, wanted_user=cadet):
                self.mahzor_names[cadet_name] = cadet_name

        self.cadet_search_box = ComboBox(self.mahzor_names, on_changed=lambda cadet: self.change_cadet(cadet))
        self.options_layout.add_component(self.cadet_search_box, 1, 0)

    def change_cadet(self, cadet):
        """
        called after choosing a cdet
        :param cadet: str. contains name of selected cadet
        :return:
        """
        self.selected_cadet = cadet
        children = []
        titles = ["ציונים אקדמיים", "שנה א'", "שנה ב'", "שנה ג'"]

        is_real_data = is_user_have_permissions(self.user, self.selected_cadet) or is_user_captain(self.user)

        all_courses_grades, all_courses_average = get_courses_of_user(self.selected_cadet, "all", is_real_data)
        self.accordion_gp_first = GridPanel(row_count=3, column_count=3, bordered=True)
        self.accordion_gp_first.add_component(Label("ממוצע כולל", bold=True), row=0, column=2)
        bg_color = bg_color_of_courses(all_courses_average)
        self.accordion_gp_first.add_component(Label(str(round(all_courses_average, 2)), bold=True), row=0, column=0,
                                              column_span=2, bg_color=bg_color)
        children.append(self.accordion_gp_first)

        for i, year in enumerate(mahzor_number_to_years[self.selected_mahzor]):
            self.accordion_gp = GridPanel(2, 1, bordered=False)
            self.accordion_gp.add_component(CadetGrades(self.user, year, self.selected_cadet,
                                                        is_real_data=is_real_data).get_ui(), 0, 0)
            self.accordion_gp.add_component(CadetSkira(self.user, year, self.selected_cadet,
                                                       is_real_data=is_real_data).get_table(), 1, 0)
            self.accordion_gp_first.add_component(Label(titles[i + 1]), row=1, column=2-i)
            self.accordion_gp_first.add_component(CadetGrades(self.user, year, self.selected_cadet,
                                                  is_real_data=is_real_data).get_ui(), row=2, column=2-i)
            children.append(self.accordion_gp)
        print(RealData)
        self.gp.add_component(Accordion(children, titles, size=SIZE_LARGE), 2, 0)
        self.gp.add_component(Button("ציוני תרגילים סמסטר נוכחי", lambda: self.gp.add_component(
            CadetExGrades(self.user, 2022, self.selected_cadet).get_table(), 4, 0)), 3, 0, bg_color='#4DDBFF')
