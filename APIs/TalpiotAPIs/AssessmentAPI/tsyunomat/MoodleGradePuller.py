from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from APIs.TalpiotAPIs.AssessmentAPI.tsyunomat.FinalGradePuller import FinalGradePuller
from sys import platform

# constants:
MOODLE_2020_LOGIN_PAGE = "https://moodle2.cs.huji.ac.il/nu{year}/auth/saml/index.php?lang=en"
MOODLE_2020_COURSES_LIST_PAGE = "https://moodle2.cs.huji.ac.il/nu{year}/grade/report/overview/index.php?lang=en"
MOODLE_2020_COURSE_GRADES_PAGE = "https://moodle2.cs.huji.ac.il/nu{year}/grade/report/user/index.php?id={course_id}&lang=en"
MOODLE_2020_COURSE_MAIN_PAGE = "https://moodle2.cs.huji.ac.il/nu{year}/course/view.php?id={course_id}&lang=en"
MOODLE_2020_MAIN_PAGE = "https://moodle2.cs.huji.ac.il/nu{year}/?lang=en"
WEB_DRIVER_WAIT_TIME = 10


class MoodleGradePuller:

    def __init__(self, row):
        self.student_name = str(row.name)

        self.cse_user = str(row.cse_user)
        self.cse_password = str(row.cse_password)
        self.id = str(row.id)
        self.password = str(row.password)

    def pull_grades(self, years=None, visible=False):
        """
        :param years: a list of years to pull grades of. if None, only current year is pulled.
        :param visible: True to make chrome driver visible, False otherwise.
        :return:
        """

        all_grades = dict()

        for year in years:

            # main action:
            table = MoodleGradePuller.get_student_table(
                id_num=self.id, password=self.password,
                cse_user=self.cse_user, cse_password=self.cse_password,
                year=year, visible=visible,
            )

            if table is None:
                raise Exception("table in moodle puller is None")

            all_grades["20" + year] = table

        return all_grades

    @staticmethod
    def get_student_table(id_num, password, cse_user, cse_password, year, visible=False):

        # Enter Website
        driver = MoodleGradePuller.login_to_moodle(year, id_num, password, visible=visible)

        yearly_courses = MoodleGradePuller.get_yearly_courses1(driver, year)

        # Get the table of exercises grades:
        courses_to_delete = []
        for course in yearly_courses:
            course_id = course['course id'].replace('-', '0')
            try:
                grades, grades_percent,\
                grades_order = MoodleGradePuller.get_course_grades(driver, cse_user, cse_password,
                                                                   year, course_id)
            except:
                courses_to_delete.append(course)
                continue

            if len(grades) > 0:
                course['grades'] = grades
                course['grades order'] = grades_order
            else:
                courses_to_delete.append(course)

        # we do not longer need more information from the web
        driver.quit()

        return [course for course in yearly_courses if course not in courses_to_delete]

    @staticmethod
    def login_to_moodle(year, id_num, password, visible):

        driver = FinalGradePuller.login(id_num, password, visible)

        # if logged in, change to english:
        driver.get(MOODLE_2020_MAIN_PAGE.format(year=year))

        driver.find_element(By.XPATH, r'/html/body/div[1]/div/div/div[2]/div/div[1]/section/div[1]/section/aside/section[1]/div/div/div[1]/div/div[1]/div[2]/form/input').click()

        return driver

    @staticmethod
    def login_to_cse(driver, cse_user, cse_password):
        driver.find_element(By.XPATH, r'/html/body/div[1]/div/div/div[2]/div/div[1]/section/div[2]/div/div[1]/div/'
                                     r'form/div[1]/div[2]/input').send_keys(cse_user)
        driver.find_element(By.XPATH, r'/html/body/div[1]/div/div/div[2]/div/div[1]/section/div[2]/div/div[1]/div/'
                                     r'form/div[1]/div[5]/input').send_keys(cse_password)
        driver.find_element(By.XPATH, r'/html/body/div[1]/div/div/div[2]/div/div[1]/section/div[2]/div/div[1]/div/'
                                     r'form/input[3]').click()

        # check if login succeeded:

        try:
            connditions = (EC.presence_of_element_located((By.LINK_TEXT, "Home")),
                           EC.presence_of_element_located((By.LINK_TEXT, "ראשי")),
                           EC.presence_of_element_located((By.LINK_TEXT, "Dashboard")))
            WebDriverWait(driver, WEB_DRIVER_WAIT_TIME).until(EC.any_of(*connditions))
        except:
            # if login failed and we stayed on the same page
            driver.quit()
            return False
        return True

    @staticmethod
    def get_yearly_courses1(driver, year):

        driver.get(MOODLE_2020_COURSES_LIST_PAGE.format(year=year))

        # check case of "Sorry, but you do not currently have permissions to do that" page
        elements = driver.find_elements(By.CLASS_NAME, "errorcode")
        if len(elements) != 0: driver.get(MOODLE_2020_COURSES_LIST_PAGE.format(year=year))

        yearly_courses = []

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "overview-grade")))
        element = driver.find_element(By.ID, "overview-grade")
        
        rows = element.find_elements(By.TAG_NAME, "tr")
        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            course_info = cells[0].text.split(" ", 1)

            if len(course_info) < 2:
                continue

            course_id = course_info[0]
            course_name = course_info[1]

            if not course_id.replace('-', '0').isdigit():
                continue

            course = {'course name': course_name,
                    'course id': course_id}

            yearly_courses.append(course)

        return yearly_courses


    @staticmethod
    def get_course_grades(driver, cse_user, cse_password, year, course_id):
        driver.get(MOODLE_2020_COURSE_GRADES_PAGE.format(year=year, course_id=course_id))

        # handle the case of "This course is currently unavailable to students":
        button_elements = driver.find_elements(By.XPATH, "//div[@class='continuebutton']")
        if len(button_elements) > 0:
            return [], [], []

        table_elements = driver.find_elements(By.XPATH, "//table[@cellspacing='0']")

        # handle cse login:
        if len(table_elements) == 0:
            logged_in = MoodleGradePuller.login_to_cse(driver, cse_user, cse_password)

            if not logged_in:
                return [], [], []

        grades_order = dict()
        grades = dict()
        grades_percent = dict()
        table_element = driver.find_elements(By.XPATH, "//table[@cellspacing='0']")[0]

        rows = table_element.find_elements(By.TAG_NAME, "tr")

        grade_ind = 4
        percent_ind = 6

        for j, row in enumerate(rows):

            cells = row.find_elements(By.TAG_NAME, "*")

            if j == 0:
                for i, c in enumerate(cells):
                    if c.text.upper() == "GRADE" or c.text == "ניקוד בפעילות":
                        grade_ind = i + 2
                    if c.text.upper() == "PERCENTAGE" or c.text == "הניקוד כאחוז מהציון המירבי בפעילות":
                        percent_ind = i + 2
                continue

            if len(cells) >= max(grade_ind, percent_ind):
                assignment_name = cells[0].text
                assignment_grade = cells[grade_ind].text
                assignment_grade_percent = cells[percent_ind].text

                if "הגשה " == assignment_name[:5] or "הגשת " == assignment_name[:5]:
                    assignment_name = assignment_name[5:]

                if "מספר " in assignment_name:
                    assignment_name = ''.join(assignment_name.split("מספר "))

                if assignment_grade.replace('.', '', 1).isdigit():
                    assignment_grade = assignment_grade.split('.')[0]
                    assignment_grade_percent = assignment_grade_percent.split('.')[0]
                    assignment_grade = str(max(int(assignment_grade), int(assignment_grade_percent)))
                    grades[assignment_name] = assignment_grade
                    grades_order[assignment_name] = j

                else:
                    assignment_url = str(cells[1].get_attribute('href'))
                    if assignment_url == 'None':
                        continue
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(assignment_url)
                    try:
                        WebDriverWait(driver, WEB_DRIVER_WAIT_TIME).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            r"/html/body/div[1]/div/div/div[2]/header/div/div/div/div[2]/div[1]/nav/ol/li[1]/a")))
                    except:
                        pass
                    table_headers = driver.find_elements(By.XPATH, '//th[@class="cell c0"]')
                    is_assignment = 'Time remaining' in [h.text for h in table_headers]
                    is_assignment = is_assignment or 'הזמן שנותר' in [h.text for h in table_headers]

                    if not is_assignment:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        continue

                    overdue = len(driver.find_elements(By.XPATH, '//td[@class="overdue cell c1"]')) == 1
                    earlysubmission = len(driver.find_elements(By.XPATH, '//td[@class="earlysubmission cell c1"]')) == 1
                    to_be_submitted = not (overdue or earlysubmission)

                    if overdue:
                        grades[assignment_name] = '0'
                        grades_percent[assignment_name] = '0'
                        grades_order[assignment_name] = j
                    elif earlysubmission or to_be_submitted:
                        grades[assignment_name] = '-'
                        grades_percent[assignment_name] = '-'
                        grades_order[assignment_name] = j

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

        # if image processing or intro to cs:
        driver.get(MOODLE_2020_COURSE_MAIN_PAGE.format(year=year, course_id=course_id))
        elements = driver.find_elements(By.XPATH, "//h5[@class='card-title d-inline']")
        # print("_____________________________________________________course admin:", len(elements))
        elements_text = [el.text for el in elements]
        # print(elements_text)
        if 'CourseAdmin' in elements_text:
            table = driver.find_element(By.XPATH, "//table[@style='width: 100%;border: 1px solid #ccc;']")
            rows = table.find_elements(By.TAG_NAME, "tr")
            for j, row in enumerate(rows):
                cells = row.find_elements(By.TAG_NAME, "*")
                # for c in cells:
                #     print(c.text, end=', ')
                # print()
                assignment_name2 = cells[2].text
                assignment_grade = cells[4].text

                if assignment_grade.replace('.', '', 1).isdigit():

                    # check if assignment already included with different name:
                    assignment_names = list(grades.keys())
                    assignment_concluded = False
                    assignment_name_ind = 0
                    for i, name in enumerate(assignment_names):
                        assignment_concluded = (name.lower() in assignment_name2.lower()) or \
                                               (assignment_name2.lower() in name.lower())
                        if assignment_concluded:
                            assignment_name_ind = i
                            break
                    if assignment_concluded:
                        name = assignment_names[assignment_name_ind]
                        grades[name] = assignment_grade
                    else:
                        grades[assignment_name2] = assignment_grade
                        grades_order[assignment_name2] = j

        return grades, grades_percent, grades_order
