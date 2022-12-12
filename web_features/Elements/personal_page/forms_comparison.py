import os
from APIs.TalpiotAPIs.AssessmentAPI.FormsReader.forms_reader import *
from web_framework.server_side.infastructure.page import Page
# standard Talpix page class to inherit from.
from APIs.ExternalAPIs.GoogleDrive.file_to_upload import FileToUpload
from web_framework.server_side.infastructure.components.all_components_import import *
from web_features.Elements.personal_page.permissions import *
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.getdata.academy_grades_interface import *


class FormsComparison(Page):
    def __init__(self, params):
        super().__init__(params)
        self.gp = None
        self.db_options = ["ממוצע ציונים"] # there is no check whether all these options exist for the cadets who answerd the form
        self.db_option = None
        self.forms_questions_list = {}
        self.forms_question = False
        self.forms_names = None
        self.forms_data = None
        self.popup = None
        self.graph_appear = False
        self.db_data = self.test_load_from_db()

    @staticmethod
    def get_title():
        return "נתוני סקרים (גרסת בטא)"

    @staticmethod
    def is_authorized(user):
        return is_user_X_admin(user) or is_user_captain(user)

    @staticmethod
    def get_group(user):
        if is_user_captain(user) or is_user_X_admin(user):
            return "All"
        if is_user_sagaz(user):
            return get_team_of_sagaz(user) + [user]
        if is_user_cadet(user):
            return [user]


    def get_page_ui(self, user: User):
        """
        returns the page's main UI component (grid panel)
        """
        self.user = user

        self.gp = GridPanel(6, 1, bordered=False)

        # added this for beta text
        self.beta_text_panel = StackPanel()
        self.beta_text_panel.add_component(
            Label("גרסה זאת היא גרסת בטא, מוזמנים לשחק ולהתרשם, נשמח לפידבק", fg_color='RED', size=SIZE_LARGE))
        self.beta_text_panel.add_component(
            HyperLink("דווחו כאן", url="https://bot.talpiot.org/react/page/suggestions", size=SIZE_MEDIUM))

        self.gp.add_component(self.beta_text_panel, 0, 0)

        # Header
        self.gp.add_component(Label("השוואת נתוני סקרים", size=SIZE_EXTRA_LARGE),1,0)
        # User Guide
        self.gp.add_component(Label("העלו לכאן טופס \"google forms\" מסוג קובץ \"csv\" ותוכלו להשוות נתונים מספריים מהטופס לנתונים השמורים במערכת\nוודאו שאחת השאלות בטופס היא \"שם ושם משפחה\""
                                    , size=SIZE_LARGE),2,0)

        self.options_layout = GridPanel(2, 3, bg_color=COLOR_PRIMARY_DARK)

        # Labels
        self.options_layout.add_component(Label("נתון מהמערכת", fg_color='White'), 0, 0)
        self.options_layout.add_component(Label("נתון מהסקר", fg_color='White'), 0, 1)
        self.options_layout.add_component(Label("סקר", fg_color='White'), 0, 2)

        # Options
        self.db_combo = ComboBox({db_option: db_option for db_option in self.db_options},
                                   on_changed=lambda db_option: self.change_db_option(db_option))
        self.options_layout.add_component(self.db_combo, 1, 0)

        self.forms_combo = ComboBox({form_que: form_que for form_que in self.forms_questions_list},
                                    on_changed=lambda forms_question: self.change_forms_question(forms_question))
        self.options_layout.add_component(self.forms_combo, 1, 1)

        # Upload box
        self.upload_slot = UploadFiles(self.upload)
        self.options_layout.add_component(self.upload_slot, 1, 2)

        self.gp.add_component(self.options_layout, 3, 0)

        return self.gp

    def upload(self, files):
        """
        this function recives the file and compiles its data, checks for errors and loads the forms questions combo box
        """
        f = FileToUpload.load_from_json(files[0])
        file_name = f.name
        self.change_forms_questions_list([[]])
        self.forms_question = False
        self.forms_names = None
        self.gp.add_component(Label(''), 4, 0)

        if not file_name.endswith('.csv'):
            self.message("הקובץ אינו מסוג csv", "שגיאה בהעלאה:")
            self.options_layout.add_component(Label("סקר", fg_color='White'), 0, 2)
            return
        with open(f.name, 'wb') as g:
            g.write(f.get_content())
        self.forms_data = read_form(file_name)
        os.remove(file_name)

        if type(self.forms_data) == str:
            self.message(self.forms_data, "שגיאה בקובץ")
            self.options_layout.add_component(Label("סקר", fg_color='White'), 0, 2)
        else:
            unknown_names, self.forms_data = self.remove_unknown_names(self.forms_data)
            if unknown_names:
                self.message(', '.join(unknown_names), 'נמחקו שמות שלא מוכרים למערכת:')
            self.options_layout.add_component(Label(f'סקר: \"{file_name}\"', fg_color='White'), 0, 2)
            self.forms_names = self.forms_data[0][1:]
            self.change_forms_questions_list(self.forms_data)


    def message(self, text, title):
        """
        this function shows a popup message with specified title and text
        """
        self.popup = PopUp(Label(text), title=title, is_shown=True, is_cancelable=True)
        self.gp.add_component(self.popup)


    def test_load_from_db(self):
        db_data = {}
        for cadet in ["דן שמשי", "עידו עברי", "רום פייביש", "מישל זילבר", "שחר זכריה"]:
                db_data[cadet] = get_courses_of_user(cadet, 2022, False)[1]
        return db_data


    def load_from_db(self, is_real_data=False):
        """
        this function will hopefully one day return a dictionary of all the cadet's relevant grades for comparison
        """

        db_data = {}
        for mahzor in [43, 42, 41]:
            for cadet in User.objects(mahzor=mahzor):
                #db_data[cadet.name] = {}

                db_data[cadet.name] = get_courses_of_user(cadet.name, 2022, is_real_data)[1]
        return db_data

    def build_graph_data(self):
        """
        returns the average grade y(x) of cadets who chose option x of a specified question from the forms
        """
        y_average = dict.fromkeys(self.forms_question, 0)
        y_count = dict.fromkeys(self.forms_question, 0)
        for num, ans in enumerate(self.forms_question):
            y_average[ans] += self.db_data[self.forms_names[num]]
            y_count[ans] += 1

        for key, val in y_average.items():
            y_average[key] = val/y_count[key]

        x_data = list(y_average)
        x_data.sort()
        y_data = [y_average[x] for x in x_data]

        return x_data, y_data

    def load_graph(self, data):
        """
        shows the bar graph of the data, where y is the average grade, x is the option from the forms
        also adds columns if the options are integers missing parts of their range
        """
        xdata = data[0]
        ydata = data[1]
        y_by_x = dict(zip(xdata, ydata))

        print(xdata)

        if self.check_if_int_list(xdata):
            xdata = self.int_list_range(xdata)
            print(xdata)

        graph = ChartjsComponent(width="50vw", height="35vw")
        buckets = [y_by_x[x] if x in y_by_x else 0 for x in xdata]
        bucket_labels = ["{0}".format(x) for x in xdata]
        graph.bar(bucket_labels, buckets, label="ממוצע", color=COLOR_PRIMARY_DARK, border_color=COLOR_PRIMARY_DARK)
        self.gp.add_component(StackPanel([graph], orientation=0), 4, 0)

        self.graph_appear = True

    def remove_unknown_names(self, forms):
        """
        checks for names who don't appear in the db
        returns those names together with a forms array excluding these names
        """
        unknown = []
        unknown_ind = []
        for name_ind, name in enumerate(forms[0][1:]):
            if name not in self.db_data:
                unknown.append(name)
                unknown_ind.append(name_ind+1)

        if unknown:
            unknown_ind.sort(reverse=True)
            for r, row in enumerate(forms):
                for ind in unknown_ind:
                    del forms[r][ind]
        return unknown, forms

    def check_if_int_list(self, list):
        """
        checks if the options for a forms question are all integers
        """
        list = [value for value in list if value != BLANK_A]
        for n in list:
            try:
                x = int(n)
            except:
                return False
        return True

    def int_list_range(self, mylist):
        """
        returns a list including the full integer range of the original, and keeps the blank answer if exists
        """
        blank = False
        for ind, val in enumerate(mylist):
            if val == BLANK_A:
                blank = ind
            else:
                mylist[ind] = int(val)
        if blank:
            del mylist[blank]

        mylist = list(range(min(mylist), max(mylist)+1))
        mylist = [str(x) for x in mylist]
        if blank:
            mylist.append(BLANK_A)
        return mylist

    def change_db_option(self, db_option):
        """
        called when a db question was chosen for comparison
        """
        self.db_option = db_option
        self.check_if_ready()

    def change_forms_question(self, forms_question):
        """
        called when a forms question was chosen for comparison
        """
        self.forms_question = self.forms_data[self.forms_questions_list.index(forms_question)+1][1:]
        self.check_if_ready()

    def change_forms_questions_list(self, forms_data):
        """
        finds all the questions from the forms, saves them to a variable and updates the combobox
        """
        self.forms_questions_list = [que[0] for que in forms_data[1:]]

        self.forms_combo = ComboBox({form_que: form_que for form_que in self.forms_questions_list},
                                    on_changed=lambda forms_question: self.change_forms_question(forms_question))

        self.options_layout.add_component(self.forms_combo, 1, 1)
        self.check_if_ready()

    def check_if_ready(self):
        """
        checks if both options for comparison are chosen, if so displays the graph
        """
        if self.db_option and self.forms_question:
            self.load_graph(self.build_graph_data())



