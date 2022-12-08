import logging
import threading
import traceback
from datetime import datetime

from tqdm import tqdm

from APIs.TalpiotAPIs.AssessmentAPI.tsyunomat.FinalGradePuller import FinalGradePuller
from APIs.TalpiotAPIs.AssessmentAPI.tsyunomat.MoodleGradePuller import MoodleGradePuller
from APIs.TalpiotAPIs.AssessmentAPI.tsyunomat.UploalDataToDB import *


class HujiGradePuller:
    def __init__(self, users_login_xlsx, is_real_data=True, update=False, wanted_year=None):
        self.__users_login_xlsx = users_login_xlsx
        self.is_real_data = is_real_data
        self.update = update
        self.wanted_year = wanted_year
        # print(users_login_xlsx)
        self.__directory_name = (list(users_login_xlsx.keys()))[0]
        self.flags = {}

    def pull_grades(self, pull_final_grades, assignments_years=None, log=True, visible=False):
        """
        :param pull_final_grades:  boolean, True to pull from final grades
        :param assignments_years: a list of the form ["19", "20"] of years
        to pull grades from (if None no assignments are pulled, -> only relevant to HW pulling)
        :param log: True for creating log (currently useless)
        :param visible: True for debugging
        :return:
        """
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        if log:  # create logger
            logger = logging.getLogger('grade_puller')
            logger.setLevel(logging.DEBUG)
            fh = logging.FileHandler('grade_puller.log')
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)

            logging.getLogger('grade_puller').info("\n" + dt_string + "\n")

        self.flags = {}
        threads = []
        for student in tqdm(self.__users_login_xlsx):
            temp_tpl = (student, self.__users_login_xlsx[student])
            args = (temp_tpl, pull_final_grades, assignments_years, log, visible)
            self.pull_student_grades(*args)
        #     t = threading.Thread(target=self.pull_student_grades, args=args)
        #     t.start()
        #     threads.append(t)
        # for t in tqdm(threads):
        #     t.join()
        return self.flags

    def pull_student_grades(self, *args):
        data, pull_final_grades, assignments_years, log, visible = args
        flag = False

        student_name = data[0]

        all_moodle_grades = None
        all_final_grades = None

        try:

            if assignments_years is not None:
                all_moodle_grades = MoodleGradePuller(data).pull_grades(years=assignments_years, visible=visible)

            if pull_final_grades:
                all_final_grades = FinalGradePuller(data).pull_grades(visible=visible, wanted_year=self.wanted_year)
                # update the list in the DB
                if all_final_grades == 'entry details':
                    print(f"problem with: {student_name} credentials")
                    return all_final_grades
            if all_moodle_grades is None and all_final_grades is None:
                raise Exception("something is wrong, log as failure")

            if log:
                logging.getLogger('grade_puller').info(f"{student_name}: Finished")
                flag = True

            upload_data_to_db(student_name, all_final_grades, is_real_data=self.is_real_data, update=self.update)
        except:
            exception_str = traceback.format_exc()
            if all_moodle_grades is None and all_final_grades is not None:
                if log:
                    logging.getLogger('grade_puller').warning(
                        f"{student_name}: Couldn't finish moodle\n{exception_str}")
                    flag = False

            # only relevant for HW
            elif all_moodle_grades is not None and all_final_grades is None:
                if log:
                    logging.getLogger('grade_puller').warning(
                        f"{student_name}: Couldn't finish final grades\n{exception_str}")
                    flag = False
                # uploading to homework_grades collection in DB
            # until here

            elif log:  # both are None
                logging.getLogger('grade_puller').warning(f"{student_name}: Couldn't finish\n{exception_str}")
                flag = False
        self.flags[student_name] = flag
        return flag
