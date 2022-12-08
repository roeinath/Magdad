from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sys import platform
from webdriver_manager.chrome import ChromeDriverManager
import time  # added to delay some code in the selenium

# constants:
LOGIN_PAGE = "https://www.huji.ac.il/dataj/controller/stu"


class FinalGradePuller:

    def __init__(self, row):
        self.student_name = row[0]
        self.cse_user = 'None'  # temporary
        self.cse_password = 'None'  # temporary
        self.email = (row[1])['email']
        self.password = (row[1])['password']

    def pull_grades(self, visible=False, wanted_year=None):
        """
        :param visible: True to make chrome driver visible, False otherwise.
        :return:
        """
        # main action:
        table = FinalGradePuller.get_student_table(huji_email=self.email, password=self.password, visible=visible,
                                                   wanted_year=wanted_year)
        return table

    @staticmethod
    def get_student_table(huji_email, password, visible, wanted_year=None):
        """
        strip the cadets data from the personal university page
        :param wanted_year: if not None - the year to pull the data from
        :param huji_email: user's university email
        :param password: user's university password
        :param visible: True for debugging
        :return: dictionary with dictionaries of course grade and data
        """
        driver = FinalGradePuller.login(huji_email, password, visible=visible)
        if driver == "entry details":
            print(f"problem with {huji_email}")
            return driver
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, "לימודים"))).click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, "קורסים וציונים"))).click()

        # switch to window on ציונים
        driver.switch_to.window(driver.window_handles[1])

        # get all the years the student spent in huji
        year_list = driver.find_element(By.XPATH, "//*[@id=\"ziyunim\"]/table[1]/tbody/tr/td[1]/select")
        years_to_options = {int(option.text.strip()): option for option in
                            year_list.find_elements(By.TAG_NAME, 'option')}

        # this table will include all the information on all the courses the student had taken
        student_table = []

        # loop through all the years
        for year in years_to_options.keys():
            if wanted_year is not None and year != wanted_year:
                continue

            # change the droplist to point on the correct year
            # TODO: check if only years_to_options is needed instead of recomputing years_to_options_local
            year_list = driver.find_element(By.XPATH, "//*[@id=\"ziyunim\"]/table[1]/tbody/tr/td[1]/select")
            years_to_options_local = {int(option.text.strip()): option for option in
                                      year_list.find_elements(By.TAG_NAME, 'option')}
            years_to_options_local[year].click()

            # get the courses for this year
            yearly_table = FinalGradePuller.get_yearly_table(driver, year)

            # add a column of year to the table
            for course in yearly_table:
                course["year"] = year

            # update the full-courses list
            student_table.extend(yearly_table)

        # we do not longer need more information from the web
        driver.quit()

        return student_table

    @staticmethod
    def login(huji_email, password, visible=False):
        # Enter Website
        options = Options()  # so chrome will be invisible
        options.headless = not visible
        options.add_argument("--log-level=3")  # show only fatal messages
        options.add_experimental_option('excludeSwitches',
                                        ['enable-logging'])  # remove "DevTools" message of chrome driver
        options.add_argument('--blink-settings=imagesEnabled=false')
        if platform == 'win32':
            driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        else:
            ser = Service(r"/usr/lib/chromium-browser/chromedriver")
            driver = webdriver.Chrome(service=ser, options=options)

        driver.get(LOGIN_PAGE)
        # enter personal log-in info , maybe need to add a delay
        driver.find_element(By.ID, "pills-email-tab").click()
        time.sleep(0.5)
        driver.find_element(By.NAME, "username").send_keys(huji_email)
        driver.find_element(By.ID, "password").send_keys(password)
        time.sleep(0.5)
        driver.find_element(By.XPATH, "//button[@data-callback = 'onSubmit3']").click()

        # check if login succeeded:
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.LINK_TEXT,
                                                "לימודים")))
        except:
            # try refreshing:
            try:
                driver.refresh()
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.LINK_TEXT,
                                                    "לימודים")))
            except:
                # if login failed and we stayed on the same page
                driver.quit()
                return "entry details"

        return driver

    @staticmethod
    def get_yearly_table(driver, year):
        # navigate in the personal page
        faculties = []
        faculty_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'" + "חוג:" + "')]")
        for el in faculty_elements:
            if el.tag_name == "strong":
                el = el.find_element(By.XPATH, "..")
            text = el.text
            text = text.strip()
            words = text.split()
            text = str.strip(''.join([s + ' ' for s in words if (not str.isnumeric(s) and not s == 'חוג:')]))
            faculties.append(text)

        yearly_courses = []
        # strip data
        elements = driver.find_elements(By.XPATH, "//table[@cellpadding='2']")
        for i, element in enumerate(elements):
            rows = element.find_elements(By.TAG_NAME, "tr")
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                course = {'course name': cells[5].text,
                          'course number': cells[6].text,
                          'naz': cells[4].text,
                          'moed': 'A',
                          'final grade': cells[3].text,
                          'semester': "A+B",
                          'grade_א': " ",
                          'grade_ב': " ",
                          'year': -1,
                          'faculty': faculties[i]}

                if 'href' in cells[1].get_attribute('innerHTML'):
                    cells[1].click()
                    driver.switch_to.window(driver.window_handles[-1])
                    found_element = True
                    element = driver.find_elements(By.XPATH, "//table[@cellpadding='2']")
                    if len(element) != 0:
                        element = element[0]
                    else:
                        found_element = False
                    if found_element:
                        subrows = element.find_elements(By.TAG_NAME, "tr")
                        all_grades = {}
                        for subrows in subrows[1:]:
                            subcells = subrows.find_elements(By.TAG_NAME, "td")
                            if subcells[3].text != 'סופי': continue
                            if subcells[1].text == "'סמסטר א":
                                course['semester'] = 'A'
                            else:
                                course['semester'] = 'B'

                            all_grades[subcells[2].text] = subcells[0].text
                        if 'א' in all_grades and 'ב' in all_grades:
                            course['moed'] = 'B'
                            course['grade_א'] = all_grades['א']
                            course['grade_ב'] = all_grades['ב']
                    last_page = driver.window_handles[-2]
                    driver.close()
                    driver.switch_to.window(last_page)

                # add mean of students grades
                course['student mean'] = " "
                if 'href' in cells[0].get_attribute('innerHTML'):
                    cells[0].click()
                    driver.switch_to.window(driver.window_handles[-1])
                    elements = driver.find_elements(By.XPATH,
                                                    r"/html/body/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/span[3]")
                    if len(elements) != 0:
                        mean = elements[0].text.split('\n')[0].split(':')[1].split()[0]
                        course['student mean'] = mean
                    last_page = driver.window_handles[-2]
                    driver.close()
                    driver.switch_to.window(last_page)

                yearly_courses.append(course)

        return yearly_courses
